"""Build the Arrhenos sketch map from the editable JSON layers in this folder.

    python build_sketch.py              # full build at 0.1 degrees (about ten minutes)
    python build_sketch.py --res 0.25   # quick draft (about two minutes)

Layers:  landmasses.json (outlines)  tectonics.json (plates)  relief.json (mountains, plateaus, coasts)
         places.json (canon cities and regions: used for checks, labels, and to pin canon coasts in place)
Outputs go to out/.  See README.md for what each one is.
"""
import argparse, json, math, os, time
import numpy as np
from PIL import Image, ImageDraw
from scipy.spatial import cKDTree
from scipy import ndimage, sparse
from scipy.sparse.linalg import splu

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")
R_KM = 6371.0

# ----------------------------------------------------------------------------- grid helpers


class Grid:
    def __init__(self, res):
        self.res = res
        self.W, self.H = int(round(360 / res)), int(round(180 / res))
        self.lon = -180 + (np.arange(self.W) + 0.5) * res
        self.lat = 90 - (np.arange(self.H) + 0.5) * res
        self.LON, self.LAT = np.meshgrid(self.lon, self.lat)
        lo, la = np.radians(self.LON), np.radians(self.LAT)
        self.xyz = np.stack([np.cos(la) * np.cos(lo), np.cos(la) * np.sin(lo), np.sin(la)], -1).astype(np.float32)
        self.dy_km = R_KM * math.radians(res)
        self.dx_km = (self.dy_km * np.cos(np.radians(self.lat)))[:, None]
        self.cell_km2 = self.dx_km * self.dy_km * np.ones((1, self.W))

    def to_px(self, pts):
        return [((lo + 180) / self.res, (90 - la) / self.res) for lo, la in pts]


def unit(lon, lat):
    lo, la = np.radians(np.asarray(lon, float)), np.radians(np.asarray(lat, float))
    return np.stack([np.cos(la) * np.cos(lo), np.cos(la) * np.sin(lo), np.sin(la)], -1)


def chord_to_km(c):
    return 2 * R_KM * np.arcsin(np.clip(c / 2, 0, 1))


def km_to_chord(d):
    return 2 * np.sin(np.minimum(d, math.pi * R_KM) / (2 * R_KM))


def raster_polys(grid, polys, holes=None, value=1):
    """Rasterise lon/lat polygons (lon may run past ±180) with wrap-around."""
    img = Image.new("L", (grid.W, grid.H), 0)
    dr = ImageDraw.Draw(img)
    for poly, hs in zip(polys, holes or [None] * len(polys)):
        for off in (-360, 0, 360):
            dr.polygon(grid.to_px([(lo + off, la) for lo, la in poly]), fill=value)
            for h in hs or []:
                dr.polygon(grid.to_px([(lo + off, la) for lo, la in h]), fill=0)
    return np.asarray(img) > 0


def densify(line, step_deg=0.05):
    """Resample a lon/lat polyline to roughly even steps (in degrees of arc)."""
    out = []
    for (a0, b0), (a1, b1) in zip(line[:-1], line[1:]):
        n = max(2, int(math.hypot((a1 - a0) * math.cos(math.radians((b0 + b1) / 2)), b1 - b0) / step_deg) + 1)
        t = np.linspace(0, 1, n, endpoint=False)
        out.extend(zip(a0 + (a1 - a0) * t, b0 + (b1 - b0) * t))
    out.append(tuple(line[-1]))
    return np.array(out)


def boundary(mask):
    """Cells of mask that touch a non-mask cell (4-neighbour, wrapping east-west)."""
    nb = np.zeros_like(mask)
    nb[1:, :] |= ~mask[:-1, :]; nb[:-1, :] |= ~mask[1:, :]
    nb |= ~np.roll(mask, 1, 1); nb |= ~np.roll(mask, -1, 1)
    return mask & nb


def nearest_edge_xyz(grid, mask, sel):
    """For the cells in sel: the unit vector of the nearest cell across mask's edge."""
    inner, outer = boundary(mask), boundary(~mask)
    pts = grid.xyz[sel]
    m_in = mask[sel]
    out = np.zeros(pts.shape, np.float32)
    for pick, src in ((m_in, grid.xyz[outer]), (~m_in, grid.xyz[inner])):
        if pick.any() and len(src):
            _, j = cKDTree(src).query(pts[pick], workers=-1)
            out[pick] = src[j]
    return out


def signed_distance(grid, mask, pts=None):
    """km to the edge of mask; positive inside. pts: optional (warped) unit vectors to measure from."""
    inner, outer = boundary(mask), boundary(~mask)
    P = grid.xyz if pts is None else pts
    inside = mask if pts is None else mask[lonlat_index(grid, pts)]
    d = np.empty(mask.shape, np.float32)
    for sel, src, sign in ((inside, outer, 1), (~inside, inner, -1)):
        if not src.any() or not sel.any():
            d[sel] = sign * 20000
            continue
        c, _ = cKDTree(grid.xyz[src]).query(P[sel], workers=-1)
        d[sel] = sign * (chord_to_km(c) - 0.5 * grid.dy_km)
    return d


def lonlat_index(grid, pts):
    """Row and column of the cell containing each unit vector."""
    lat = np.degrees(np.arcsin(np.clip(pts[..., 2], -1, 1)))
    lon = np.degrees(np.arctan2(pts[..., 1], pts[..., 0]))
    i = np.clip(((90 - lat) / grid.res).astype(int), 0, grid.H - 1)
    j = (((lon + 180) / grid.res).astype(int)) % grid.W
    return i, j


def bbox_mask(grid, lonlats, margin_km):
    """Cells within a lon/lat box around the given points (lon may run past ±180), or None for 'everywhere'."""
    ll = np.asarray(lonlats, float).reshape(-1, 2)
    lon = np.degrees(np.unwrap(np.radians(ll[:, 0])))
    m_lat = margin_km / 111.2
    la0, la1 = ll[:, 1].min() - m_lat, ll[:, 1].max() + m_lat
    if la0 <= -85 or la1 >= 85:
        return None
    m_lon = margin_km / (111.2 * math.cos(math.radians(max(abs(la0), abs(la1)))))
    lo0, lo1 = lon.min() - m_lon, lon.max() + m_lon
    if lo1 - lo0 >= 350:
        return None
    rows = (grid.lat >= la0) & (grid.lat <= la1)
    cols = ((grid.lon - lo0) % 360 + lo0) <= lo1
    return rows[:, None] & cols[None, :]


def line_distance(grid, lines, max_km, pts=None, slack_km=0):
    """Distance (km) from every cell to the nearest of the polylines, capped at max_km.

    Returns (dist, idx, frac): idx is the nearest line (-1 if none), frac the position along it (0-1).
    slack_km widens the search box when pts are warped."""
    shp = grid.LAT.shape
    sel = bbox_mask(grid, np.concatenate([np.asarray(l, float) for l in lines]), max_km + slack_km)
    if sel is not None and sel.sum() < 0.6 * sel.size:
        dist = np.full(shp, max_km, np.float32); idx = np.full(shp, -1, np.int32); frac = np.zeros(shp, np.float32)
        P = (grid.xyz if pts is None else pts)[sel]
        d, i, f = _line_query(grid, lines, max_km, P)
        dist[sel], idx[sel], frac[sel] = d, i, f
        return dist, idx, frac
    P = (grid.xyz if pts is None else pts).reshape(-1, 3)
    d, i, f = _line_query(grid, lines, max_km, P)
    return d.reshape(shp), i.reshape(shp), f.reshape(shp)


def _line_query(grid, lines, max_km, P):
    src, ids, fr = [], [], []
    for k, ln in enumerate(lines):
        dl = densify(ln, 0.25 * grid.res + 0.02)
        src.append(unit(dl[:, 0], dl[:, 1])); ids.append(np.full(len(dl), k)); fr.append(np.linspace(0, 1, len(dl)))
    src, ids, fr = np.concatenate(src), np.concatenate(ids), np.concatenate(fr)
    c, j = cKDTree(src).query(P, distance_upper_bound=float(km_to_chord(max_km)), workers=-1)
    ok = np.isfinite(c)
    dist = np.full(c.shape, max_km, np.float32); dist[ok] = chord_to_km(c[ok])
    idx = np.full(c.shape, -1, np.int32); idx[ok] = ids[j[ok]]
    frac = np.zeros(c.shape, np.float32); frac[ok] = fr[j[ok]]
    return dist, idx, frac


def point_distance(grid, lonlat, max_km, pts=None):
    """Distance (km) to the nearest of a set of points, and which one."""
    ll = np.asarray(lonlat, float).reshape(-1, 2)
    shp = grid.LAT.shape
    sel = bbox_mask(grid, ll, max_km) if len(ll) < 50 else None
    if sel is None:
        sel = np.ones(shp, bool)
    P = (grid.xyz if pts is None else pts)[sel]
    c, j = cKDTree(unit(ll[:, 0], ll[:, 1])).query(P, distance_upper_bound=float(km_to_chord(max_km)), workers=-1)
    ok = np.isfinite(c)
    dist = np.full(shp, max_km, np.float32); idx = np.full(shp, -1, np.int32)
    dd = np.full(c.shape, max_km, np.float32); dd[ok] = chord_to_km(c[ok])
    ii = np.full(c.shape, -1, np.int32); ii[ok] = j[ok]
    dist[sel], idx[sel] = dd, ii
    return dist, idx


def smoothstep(x):
    x = np.clip(x, 0, 1)
    return x * x * (3 - 2 * x)


def warp_points(grid, w):
    """Unit vectors displaced by a warp field (N,3) and renormalised."""
    p = grid.xyz.reshape(-1, 3) + w
    return (p / np.linalg.norm(p, axis=1, keepdims=True)).astype(np.float32).reshape(grid.xyz.shape)


# ----------------------------------------------------------------------------- noise


class Perlin3:
    """Improved Perlin gradient noise in 3D, vectorised; sampled on the unit sphere so there are no seams."""
    G = np.array([[1, 1, 0], [-1, 1, 0], [1, -1, 0], [-1, -1, 0], [1, 0, 1], [-1, 0, 1], [1, 0, -1], [-1, 0, -1],
                  [0, 1, 1], [0, -1, 1], [0, 1, -1], [0, -1, -1]], np.float32)

    def __init__(self, seed):
        p = np.random.default_rng(seed).permutation(256)
        self.p = np.concatenate([p, p]).astype(np.int32)

    def _g(self, h, x, y, z):
        g = self.G[h % 12]
        return g[..., 0] * x + g[..., 1] * y + g[..., 2] * z

    def __call__(self, P):
        out = np.empty(P.shape[0], np.float32)
        step = 1 << 20
        for s in range(0, P.shape[0], step):
            x, y, z = (P[s:s + step, k] for k in range(3))
            X, Y, Z = np.floor(x), np.floor(y), np.floor(z)
            x, y, z = (x - X).astype(np.float32), (y - Y).astype(np.float32), (z - Z).astype(np.float32)
            X, Y, Z = X.astype(np.int64) & 255, Y.astype(np.int64) & 255, Z.astype(np.int64) & 255
            u, v, w = (t * t * t * (t * (t * 6 - 15) + 10) for t in (x, y, z))
            p = self.p
            A = p[X] + Y; AA = p[A] + Z; AB = p[A + 1] + Z
            B = p[X + 1] + Y; BA = p[B] + Z; BB = p[B + 1] + Z
            g1 = self._g(p[AA], x, y, z); l1 = g1 + u * (self._g(p[BA], x - 1, y, z) - g1)
            g2 = self._g(p[AB], x, y - 1, z); l2 = g2 + u * (self._g(p[BB], x - 1, y - 1, z) - g2)
            g3 = self._g(p[AA + 1], x, y, z - 1); l3 = g3 + u * (self._g(p[BA + 1], x - 1, y, z - 1) - g3)
            g4 = self._g(p[AB + 1], x, y - 1, z - 1); l4 = g4 + u * (self._g(p[BB + 1], x - 1, y - 1, z - 1) - g4)
            m1 = l1 + v * (l2 - l1); m2 = l3 + v * (l4 - l3)
            out[s:s + step] = m1 + w * (m2 - m1)
        return out


class Noise:
    def __init__(self, grid, seed):
        self.grid, self.seed = grid, seed
        self.P = grid.xyz.reshape(-1, 3)
        self.max_freq = 0.9 * R_KM / grid.dy_km  # stop before the grid resolution

    PERLIN_STD = 0.27  # measured spread of a single octave on the sphere

    def fbm(self, freq, octaves, gain=0.5, lac=2.0, seed=0, warp=None):
        """Fractal noise with a standard deviation of 0.5 (so roughly within ±1.5).

        freq is in cycles per planet radius: 1 gives ~6,000 km features, 50 gives ~130 km."""
        P = self.P if warp is None else self.P + warp
        tot, amp, sq, f = np.zeros(P.shape[0], np.float32), 1.0, 0.0, freq
        for o in range(octaves):
            if f > self.max_freq:
                break
            tot += amp * Perlin3(self.seed * 1000 + seed * 37 + o)(P * f + o * 17.3)
            sq += amp * amp; amp *= gain; f *= lac
        return (0.5 * tot / (math.sqrt(max(sq, 1e-9)) * self.PERLIN_STD)).reshape(self.grid.LAT.shape)

    def fbm_pts(self, P, freq, octaves, gain=0.5, lac=2.0, seed=0):
        """Like fbm, but at arbitrary unit vectors P (N, 3); returns a flat array."""
        tot, amp, sq, f = np.zeros(P.shape[0], np.float32), 1.0, 0.0, freq
        for o in range(octaves):
            if f > self.max_freq:
                break
            tot += amp * Perlin3(self.seed * 1000 + seed * 37 + o)(P * f + o * 17.3)
            sq += amp * amp; amp *= gain; f *= lac
        return 0.5 * tot / (math.sqrt(max(sq, 1e-9)) * self.PERLIN_STD)

    def rmf(self, freq, octaves, seed=0, H=0.85, lac=2.0, gain=2.2, warp=None):
        """Ridged multifractal (Musgrave): sharp crests, smooth valleys, in [0, 1]."""
        P = self.P if warp is None else self.P + warp
        tot = np.zeros(P.shape[0], np.float32); wgt = np.ones(P.shape[0], np.float32)
        norm, f = 0.0, freq
        for o in range(octaves):
            if f > self.max_freq:
                break
            n = Perlin3(self.seed * 1000 + seed * 53 + o + 500)(P * f + o * 7.7)
            sig = np.clip(1.0 - 1.45 * np.abs(n), 0, 1) ** 2 * wgt
            wgt = np.clip(sig * gain, 0, 1)
            a = (f / freq) ** (-H)
            tot += sig * a; norm += a
            f *= lac
        return (tot / norm * 1.35).clip(0, 1).reshape(self.grid.LAT.shape)

    def warp_field(self, freq, amp, seed, octaves=4):
        return (np.stack([self.fbm(freq, octaves, seed=seed + k).reshape(-1) for k in range(3)], -1) * amp).astype(np.float32)


# ----------------------------------------------------------------------------- load layers


def load(name):
    with open(os.path.join(HERE, name), encoding="utf-8") as fh:
        return json.load(fh)


# ----------------------------------------------------------------------------- build


def build(res, seed, stages):
    t0 = time.time()
    grid = Grid(res)
    L, T, RL, PL = load("landmasses.json"), load("tectonics.json"), load("relief.json"), load("places.json")
    noise = Noise(grid, seed)
    log = lambda m: print(f"[{time.time() - t0:6.1f}s] {m}", flush=True)
    r = dict(grid=grid, L=L, T=T, RL=RL, PL=PL, probes={})

    # ---- control masks
    seas = [f for f in L["water"] if f.get("kind") != "lake"]
    lakes = [f for f in L["water"] if f.get("kind") == "lake"]
    big = [f for f in L["land"] if not f.get("kind")]
    isles = [f for f in L["land"] if f.get("kind")]
    land0 = raster_polys(grid, [f["polygon"] for f in big], [f.get("holes") for f in big])
    water = raster_polys(grid, [f["polygon"] for f in seas], [f.get("holes") for f in seas])
    straits = [f for f in seas if f.get("kind") == "strait"]
    core = ndimage.binary_erosion(water, iterations=max(1, int(round(35 / grid.dy_km))))
    forced_water = core | (raster_polys(grid, [f["polygon"] for f in straits]) if straits else False)
    lake = raster_polys(grid, [f["polygon"] for f in lakes]) if lakes else np.zeros_like(land0)
    isle_mask = raster_polys(grid, [f["polygon"] for f in isles]) if isles else np.zeros_like(land0)
    land0 = (land0 & ~water) | isle_mask

    # ---- anchors: canon places and spaceport sites keep their coasts where the outlines put them
    anchors = [(c["lon"], c["lat"]) for c in PL["cities"]] + [(s["lon"], s["lat"]) for s in PL["spaceport_sites"]]
    d_anchor, _ = point_distance(grid, anchors, 1500)
    calm_anchor = np.exp(-(d_anchor / 260) ** 2)
    pinned = [(c["lon"], c["lat"]) for c in PL["cities"] if c.get("coastal")]
    if pinned:  # canon coastal cities: the coast stays exactly where the outline puts it
        d_pin, _ = point_distance(grid, pinned, 1500)
        calm_anchor = np.maximum(calm_anchor, np.exp(-(d_pin / 330) ** 4))

    # ---- coast styles
    style_names = ["fjord", "skerry", "smooth", "rift", "delta", "tidal", "inland", "strait"]
    zone = {s: np.zeros(grid.LAT.shape, np.float32) for s in style_names}
    for z in RL["coast_zones"]:
        zone[z["style"]] = np.maximum(zone[z["style"]], raster_polys(grid, [z["polygon"]]).astype(np.float32))
    for s in style_names:
        zone[s] = ndimage.gaussian_filter(zone[s], sigma=1.2 / res, mode=("nearest", "wrap"))
    calm = np.clip(zone["smooth"] + 0.7 * zone["rift"] + zone["delta"] + zone["tidal"] + 0.4 * zone["inland"]
                   + zone["strait"], 0, 1)
    glacial = np.clip(zone["fjord"] + zone["skerry"], 0, 1)
    log("control masks")

    # ---- coastline: warp the outlines a little, then add fractal detail
    big_warp = noise.warp_field(2.2, 0.016, seed=11) + noise.warp_field(6.0, 0.006, seed=14)
    big_warp *= (1 - 0.97 * calm_anchor).reshape(-1, 1)
    sd = signed_distance(grid, land0, warp_points(grid, big_warp))
    log("warped coast distance")
    amp = 115 * (1 - 0.6 * calm) * (1 - 0.95 * calm_anchor)
    cw = noise.warp_field(4.0, 0.03, seed=21)
    n_coast = noise.fbm(5.0, 11, gain=0.7, seed=1, warp=cw)
    P = sd + amp * n_coast
    if glacial.max() > 0:
        # Fjords: glacial troughs run inland, square to the coast. Sampling the noise at each cell's nearest
        # coast point makes it constant along lines normal to the shore; a small warp lets troughs bend and fork.
        sel = (glacial > 0.15) & (np.abs(P) < 320)
        q = nearest_edge_xyz(grid, P > 0, sel)
        wig = noise.warp_field(20.0, 0.006, seed=32).reshape(grid.xyz.shape)[sel]
        inland = np.clip(P[sel], 0, 300)[:, None] / 300
        q = q + wig * inland
        q /= np.linalg.norm(q, axis=1, keepdims=True)
        nf = noise.fbm_pts(q, 46.0, 3, gain=0.5, seed=3) + 0.5 * noise.fbm_pts(q, 110.0, 2, seed=33)
        channel = 1 - smoothstep(np.abs(nf) / 0.22)
        reach = np.exp(-np.maximum(P[sel], 0) / (90 + 80 * zone["fjord"][sel]))
        P[sel] = P[sel] - glacial[sel] * channel * reach * 160 * (1 - calm_anchor[sel])
        sk = noise.fbm(55.0, 3, seed=4)
        P = np.where((P < 0) & (P > -40) & (sk > 0.85) & (glacial > 0.3), 4.0, P)
    land = (P > 0) & ~forced_water
    land |= isle_mask & (P > -60)  # small islands survive the noise
    d, _ = point_distance(grid, anchors, 60)  # canon places are on land
    land |= (d < 25) & ~forced_water
    land = remove_specks(land)
    if lakes:  # lake shores get the same kind of wobble as coasts
        lake = ((signed_distance(grid, lake) + 30 * n_coast) > 0) & land
    Pc = np.where(land, np.maximum(P, 1.0), np.minimum(P, -1.0)).astype(np.float32)
    log("coastline")

    # ---- tectonic distances
    B = T["boundaries"]
    kinds = {k: [b["line"] for b in B if b["kind"] == k] for k in ("ridge", "rift", "trench", "transform")}
    d_ridge, _, _ = line_distance(grid, kinds["ridge"] + kinds["rift"], 4000)
    d_trench, _, _ = line_distance(grid, kinds["trench"], 1500)
    d_rift, _, _ = line_distance(grid, kinds["rift"], 1500)
    log("tectonic distances")

    # ---- ocean floor
    blur = ndimage.gaussian_filter(land.astype(np.float32), sigma=60 / grid.dy_km, mode=("nearest", "wrap"))
    general = land | (blur > 0.3)
    sd_gen = signed_distance(grid, general)
    o = np.where(land, 0, np.maximum(-sd_gen, 0) + 0.25 * (-np.minimum(Pc, 0)))
    shelf = 130 - 110 * np.exp(-d_trench / 260) - 95 * np.exp(-d_rift / 150)
    shelf = np.clip(shelf * (0.2 + 1.6 * np.clip(noise.fbm(4.0, 4, seed=5) * 0.5 + 0.5, 0, 1.2)) + 80 * glacial, 10, 420)
    dr = np.sqrt(d_ridge ** 2 + 130 ** 2) - 130
    abyss = -2500 - 3000 * np.sqrt(np.clip(dr / 2600, 0, 1))
    shelf_h = -(12 + 118 * np.clip(o / shelf, 0, 1) ** 1.3)
    slope_t = smoothstep((o - shelf) / 110)
    deep_t = smoothstep((o - shelf - 100) / 450)
    ocean = shelf_h * (1 - slope_t) - 3100 * slope_t
    ocean = ocean * (1 - deep_t) + np.minimum(abyss, -2700) * deep_t
    ocean += -3800 * np.exp(-(d_trench / 45) ** 2) * smoothstep((o - 30) / 70)
    shallow = np.clip(zone["tidal"] + zone["inland"], 0, 1)
    ocean = ocean * (1 - shallow) + np.maximum(ocean, -40 - 90 * smoothstep(o / 150)) * shallow
    hills = noise.rmf(22.0, 4, seed=9)
    ocean += deep_t * ((380 * np.exp(-dr / 700) + 140) * (hills - 0.45))
    rng = np.random.default_rng(seed + 99)
    nsm = int(4 * math.pi * R_KM ** 2 / 350000)
    zs = rng.uniform(-1, 1, nsm); th = rng.uniform(-math.pi, math.pi, nsm)
    smts = np.stack([np.degrees(th), np.degrees(np.arcsin(zs))], -1)
    dsm, ism = point_distance(grid, smts, 120)
    hsm = rng.uniform(900, 3200, nsm); rsm = rng.uniform(14, 38, nsm)
    ok = ism >= 0
    cone = np.zeros_like(dsm)
    cone[ok] = hsm[ism[ok]] * np.clip(1 - dsm[ok] / rsm[ism[ok]], 0, 1) ** 1.5
    ocean += cone * deep_t
    for hs in T["hotspots"]:
        dh, _, _ = line_distance(grid, [hs["track"]], 1500)
        ocean += 1400 * np.exp(-(dh / 420) ** 2)
    log("ocean floor")

    # ---- land
    p_in = np.maximum(Pc, 0)
    h = 15 + 250 * (1 - np.exp(-p_in / 400)) + 0.03 * p_in
    reg = noise.fbm(2.4, 4, seed=12)
    h += np.where(reg > 0, 360 * reg, 140 * reg) * smoothstep(p_in / 200)  # regional highlands and basins
    h += 90 * noise.fbm(9.0, 8, gain=0.55, seed=6) * smoothstep(p_in / 60)
    h = np.maximum(h, 8 + 0.02 * p_in)
    probe(r, "base", h)
    rw = noise.warp_field(7.0, 0.018, seed=41)
    rpts = warp_points(grid, rw)
    width_n = noise.fbm(5.0, 3, seed=42)
    along_n = noise.fbm(8.0, 3, seed=43)
    tex_young = noise.rmf(11.0, 8, seed=44, warp=noise.warp_field(18.0, 0.004, seed=45))
    tex_old = 0.5 * noise.rmf(8.0, 6, seed=46, H=1.0) + 0.5 * (noise.fbm(12.0, 6, seed=47) * 0.3 + 0.5)
    for rg in RL["ranges"]:
        w = rg["width"]
        d, _, frac = line_distance(grid, [rg["line"]], 3.6 * w, pts=rpts, slack_km=150)
        if not (d < 3.6 * w).any():
            continue
        wv = w * (1 + 0.35 * width_n)
        fade = smoothstep((3.6 * w - d) / (0.9 * w))
        core = np.exp(-(d / wv) ** 2); foot = np.exp(-(d / (2.3 * wv)) ** 2) * fade
        taper = 0.3 + 0.7 * smoothstep(frac / 0.07) * smoothstep((1 - frac) / 0.07)
        uplift = rg["height"] * (0.72 * core + 0.28 * foot) * taper * np.clip(0.78 + 0.4 * along_n, 0.3, 1.25)
        st = rg["style"]
        if st in ("young", "glacial"):
            add = uplift * (0.28 + 1.0 * tex_young)
        elif st == "volcanic":
            add = uplift * 0.45 * (0.6 + 0.6 * tex_old) + volcano_string(grid, rg, rng)
        elif st == "rift":
            add = uplift * (0.55 + 0.6 * tex_old)
        else:
            add = uplift * (0.35 + 0.9 * tex_old)
        if rg.get("submarine"):
            ocean += np.where(~land, 0.9 * add, 0)
            h += np.where(land, 0.7 * add, 0)
        else:
            h += np.where(land, add, 0)
            ocean += np.where(~land, 0.4 * add, 0)
    probe(r, "ranges", h)
    for v in RL.get("volcanoes", []):
        d, _ = point_distance(grid, [(v["lon"], v["lat"])], 3 * v["radius"])
        cone = v["height"] * np.clip(1 - d / v["radius"], 0, 1) ** 1.3
        h += np.where(land, cone, 0)
        ocean += np.where(~land, 0.5 * cone + 2000 * np.exp(-(d / v["radius"]) ** 2), 0)
    for f in L["land"]:  # small volcanic islands get a cone
        if f.get("kind") in ("arc", "hotspot", "ridge"):
            c = np.array(f["polygon"]).mean(0)
            d, _ = point_distance(grid, [tuple(c)], 300)
            h += np.where(land, 1300 * np.exp(-(d / 35) ** 2), 0)
            ocean += np.where(~land, 2400 * np.exp(-(d / 90) ** 2), 0)
    pw = noise.warp_field(5.0, 0.016, seed=51) + noise.warp_field(14.0, 0.01, seed=53)
    pwarp = warp_points(grid, pw * (1 - calm_anchor).reshape(-1, 1))
    ragged = noise.fbm(22.0, 4, seed=54) + 1.3 * noise.fbm(7.0, 3, seed=55)
    rolling = noise.fbm(10.0, 5, seed=56)
    dissect = noise.rmf(16.0, 5, seed=52)
    for pl in RL["plateaus"]:
        m = raster_polys(grid, [pl["polygon"]])
        if not m.any():
            continue
        dp = signed_distance(grid, m, pwarp) + 0.6 * pl["scarp"] * ragged
        s = pl["scarp"]
        lift = pl["height"] * smoothstep((dp + 0.5 * s) / s)
        edge = np.exp(-(dp / (0.8 * s)) ** 2)
        lift *= 1 - 0.55 * edge * (1 - dissect)
        flat = 0.75 if "flat" in pl.get("style", "") else 0.85
        inside = smoothstep(dp / s)
        gorges = 1 - smoothstep(dissect / 0.22)  # rivers cut down into the tableland
        top = inside * (0.14 * pl["height"] * rolling - 0.3 * pl["height"] * gorges)
        h = np.where(land, h * (1 - (1 - flat) * inside) + lift + top, h)
    probe(r, "plateaus", h)
    for b in RL["basins"]:
        if "line" in b:
            d, _, _ = line_distance(grid, [b["line"]], 3 * b["radius"], pts=rpts, slack_km=150)
        else:
            d, _ = point_distance(grid, [(b["lon"], b["lat"])], 3 * b["radius"] + 150, pts=rpts)
        wgt = np.exp(-(d / b["radius"]) ** 2)
        tgt = b["level"] + 120 * (noise.fbm(20.0, 3, seed=61) * 0.5 + 0.5)
        h = np.where(land, h + (np.minimum(h, tgt) - h) * wgt, h)
    h = np.maximum(h, 2)
    probe(r, "basins", h)
    log("land relief")

    # ---- ice sheets
    ice = np.zeros_like(h)
    mw = noise.fbm(7.0, 5, seed=71)
    for s in RL.get("ice_sheets", []):
        mg = np.array(s["margin"], float)
        lon_u = np.where(grid.LON < mg[0, 0], grid.LON + 360, grid.LON)
        m_lat = np.interp(lon_u, mg[:, 0], mg[:, 1]) + 2.2 * mw
        inside = land & (grid.LAT >= m_lat)
        if inside.any():
            di = signed_distance(grid, inside)
            ice = np.maximum(ice, s["thickness"] * np.sqrt(np.clip(di / 900, 0, 1)) * inside)
    h = np.where(ice > 0, h * 0.55 + ice, h)
    log("ice")

    # ---- lakes sit a little below the surrounding land
    if lake.any():
        lab, n = ndimage.label(lake)
        for k in range(1, n + 1):
            m = lab == k
            ring = ndimage.binary_dilation(m, iterations=3) & ~m & land
            lvl = np.percentile(h[ring], 10) - 15 if ring.any() else 150
            h[m] = max(lvl, 5)
    elev = np.where(land, h, np.minimum(ocean, -5)).astype(np.float32)
    r.update(elev=elev, land=land, lake=lake, ice=ice > 1, sd=sd, zone=zone, water=water)
    if "circulation" in stages:
        r["circ"] = circulation(grid, land)
        log("circulation")
    return r


def probe(r, stage, h):
    g = r["grid"]
    for c in r["PL"]["cities"]:
        lon = (c["lon"] + 180) % 360 - 180
        i, j = min(int((90 - c["lat"]) / g.res), g.H - 1), int((lon + 180) / g.res) % g.W
        r["probes"].setdefault(c["name"], {})[stage] = float(h[i, j])


def volcano_string(grid, rg, rng):
    """A chain of cones along a volcanic line."""
    dl = densify(rg["line"], 0.05)
    seg = np.hypot(np.diff(dl[:, 0]) * np.cos(np.radians(dl[:-1, 1])), np.diff(dl[:, 1])) * 111.2
    cum = np.concatenate([[0], np.cumsum(seg)])
    pos, s = [], rng.uniform(20, 60)
    while s < cum[-1]:
        k = np.searchsorted(cum, s)
        k = min(k, len(dl) - 1)
        off = rng.normal(0, 0.18 * rg["width"]) / 111.2
        pos.append((dl[k, 0] + off / max(math.cos(math.radians(dl[k, 1])), 0.2), dl[k, 1] + rng.normal(0, 0.1) * off * 3))
        s += rng.uniform(55, 130)
    if not pos:
        return 0
    d, idx = point_distance(grid, pos, 80)
    hc = rng.uniform(0.45, 1.0, len(pos)) * rg["height"]
    rc = rng.uniform(18, 38, len(pos))
    out = np.zeros_like(d)
    ok = idx >= 0
    out[ok] = hc[idx[ok]] * np.clip(1 - d[ok] / rc[idx[ok]], 0, 1) ** 1.4
    return out


def remove_specks(land, min_cells=3):
    lab, n = ndimage.label(land)
    sizes = ndimage.sum(land, lab, index=np.arange(1, n + 1))
    land = land & ~np.isin(lab, np.nonzero(sizes < min_cells)[0] + 1)
    lab, n = ndimage.label(~land)  # fill tiny ponds
    sizes = ndimage.sum(~land, lab, index=np.arange(1, n + 1))
    return land | np.isin(lab, np.nonzero(sizes < min_cells)[0] + 1)


# ----------------------------------------------------------------------------- winds and currents

OMEGA = 2 * math.pi / (20 * 3600) * (1 + 1 / 365)  # a 20-hour day
HADLEY, POLAR_FRONT = 27.0, 57.0  # a faster spin narrows the Hadley cell a little (~30° and ~60° on Earth)


def wind_profile(lat):
    """Idealised annual-mean surface winds: (u east, v north) in m/s."""
    a = np.abs(lat)
    u = np.interp(a, [0, 6, 14, 22, HADLEY, 36, 46, 52, POLAR_FRONT, 66, 78, 90],
                  [-3.0, -5.5, -6.5, -4.5, 0.0, 5.5, 8.5, 7.0, 0.0, -2.5, -2.0, 0.0])
    u = np.where(lat < 0, u * np.interp(a, [0, 27, 45, 90], [1, 1, 1.35, 1.2]), u)  # stronger southern westerlies
    v_mag = np.interp(a, [0, 4, 14, HADLEY, 36, 50, POLAR_FRONT, 70, 90], [0, 1.2, 2.2, 0, 1.0, 1.0, 0, -1.0, 0])
    v = np.where(a < HADLEY, -np.sign(lat) * v_mag, np.sign(lat) * v_mag)
    v = np.where(a > POLAR_FRONT, np.sign(lat) * v_mag, v)
    return u, v


def circulation(grid, land):
    """Wind-driven barotropic ocean circulation: Stommel model with the island rule, on a 1° grid."""
    k = max(1, int(round(1.0 / grid.res)))
    H, W = grid.H // k, grid.W // k
    lm = land[:H * k, :W * k].reshape(H, k, W, k).mean((1, 3)) > 0.5
    lat = 90 - (np.arange(H) + 0.5) * (180 / H)
    lm[np.abs(lat) > 84] = True
    lab = wrap_label(lm, np.ones((3, 3)))
    olab = wrap_label(~lm, None)
    sizes = ndimage.sum(~lm, olab, index=np.arange(1, olab.max() + 1))
    ocean = olab == (np.argmax(sizes) + 1)  # the connected world ocean; land-locked seas are left out
    islands = [v for v in np.unique(lab[lm]) if v]
    ref = lab[0, 0]
    a = R_KM * 1000
    phi = np.radians(lat)
    dphi, dlam = math.radians(180 / H), math.radians(360 / W)
    beta = 2 * OMEGA * np.cos(phi) / a
    r = 2 * OMEGA / a * 190e3  # Stommel boundary layer ~190 km wide at the equator
    rho = 1025.0
    u10, _ = wind_profile(lat)
    tau = 1.2e-3 * 1.25 * np.abs(u10) * u10 * 1.4  # N/m2, rough bulk formula
    tc = tau * np.cos(phi)
    curl = np.zeros(H)  # curl = -1/(a cos) d(tau cos)/dphi; rows run north to south
    curl[1:-1] = (tc[2:] - tc[:-2]) / (2 * dphi) / (a * np.cos(phi[1:-1]))
    idx = -np.ones((H, W), int)
    idx[ocean] = np.arange(ocean.sum())
    N = ocean.sum()
    rows, cols, vals = [], [], []
    rhs0 = np.zeros(N)
    bnd = {}
    cos_n = np.cos(phi + dphi / 2); cos_s = np.cos(phi - dphi / 2)
    for i, j in zip(*np.nonzero(ocean)):
        p = idx[i, j]
        cp = math.cos(phi[i])
        cx = r / (a * a * cp * cp * dlam * dlam)
        cn = r * cos_n[i] / (a * a * cp * dphi * dphi)
        cs = r * cos_s[i] / (a * a * cp * dphi * dphi)
        bx = beta[i] / (a * cp * 2 * dlam)
        rows.append(p); cols.append(p); vals.append(-2 * cx - cn - cs)
        for ni, nj, c in ((i, (j + 1) % W, cx + bx), (i, (j - 1) % W, cx - bx), (i - 1, j, cn), (i + 1, j, cs)):
            if ocean[ni, nj]:
                rows.append(p); cols.append(idx[ni, nj]); vals.append(c)
            else:
                bnd.setdefault(lab[ni, nj] if lm[ni, nj] else -1, []).append((p, c))
        rhs0[p] = curl[i] / rho
    lu = splu(sparse.csc_matrix((vals, (rows, cols)), shape=(N, N)))
    psi0 = lu.solve(rhs0)
    free = [s for s in islands if s != ref]
    basis = []
    for s in free:
        b = np.zeros(N)
        for p, c in bnd.get(s, []):
            b[p] -= c
        basis.append(lu.solve(b))
    # island rule: r * (circulation of transport around the coast) = circulation of wind stress / rho
    M = np.zeros((len(free), len(free))); rhs = np.zeros(len(free))
    for m, s in enumerate(free):
        circ = 0.0
        for i, j in np.argwhere(lab == s):
            cp = math.cos(phi[i])
            for ni, nj, kind in ((i, (j + 1) % W, "e"), (i, (j - 1) % W, "w"), (i - 1, j, "n"), (i + 1, j, "s")):
                if not (0 <= ni < H and ocean[ni, nj]):
                    continue
                p = idx[ni, nj]
                if kind in "ew":
                    dl, dn, tt = a * dphi, a * cp * dlam, 0.0
                else:
                    dl, dn = a * cp * dlam, a * dphi
                    tt = -tau[i] if kind == "n" else tau[i]
                wgt = dl / dn
                M[m, m] -= r * wgt
                for q in range(len(free)):
                    M[m, q] += r * wgt * basis[q][p]
                rhs[m] -= r * wgt * psi0[p]
                circ += tt * dl / rho
        rhs[m] += circ
    cvals = np.linalg.solve(M, rhs) if free else []
    psi = psi0 + sum(c * bv for c, bv in zip(cvals, basis))
    PSI = np.zeros((H, W))
    PSI[ocean] = psi
    for c, s in zip(cvals, free):
        PSI[lab == s] = c
    dpsi_dy = np.gradient(PSI, axis=0) / (-a * dphi)
    dpsi_dx = (np.roll(PSI, -1, 1) - np.roll(PSI, 1, 1)) / (2 * a * np.cos(phi)[:, None] * dlam)
    U, V = -dpsi_dy / 1000, dpsi_dx / 1000  # m/s, taking a 1 km deep wind-driven layer
    U[~ocean] = 0; V[~ocean] = 0
    PSI[~ocean & ~lm] = np.nan
    return dict(lat=lat, lon=-180 + (np.arange(W) + 0.5) * (360 / W), psi=PSI / 1e6, U=U, V=V, ocean=ocean,
                land=lm, islands=len(islands))


def wrap_label(mask, structure):
    lab, n = ndimage.label(mask, structure=structure)
    changed = True
    while changed:
        changed = False
        for i in range(mask.shape[0]):
            a, b = lab[i, 0], lab[i, -1]
            if a and b and a != b:
                lab[lab == max(a, b)] = min(a, b); changed = True
    return lab


# ----------------------------------------------------------------------------- canon checks


def checks(r):
    g, elev, land, PL = r["grid"], r["elev"], r["land"], r["PL"]
    lines = ["# Canon checks", "", f"Built at {g.res}° ({g.W} × {g.H}).", ""]

    def at(lon, lat):
        lon = (lon + 180) % 360 - 180
        return min(int((90 - lat) / g.res), g.H - 1), int((lon + 180) / g.res) % g.W

    d_land = signed_distance(g, land)
    for c in PL["cities"]:
        i, j = at(c["lon"], c["lat"])
        ok = land[i, j]
        lines.append(f"- {'ok ' if ok else 'FAIL'} **{c['name']}** ({c['lat']}°, {c['lon']}°): {'land' if ok else 'SEA'}, "
                     f"{elev[i, j]:.0f} m, {abs(d_land[i, j]):.0f} km from the sea. Canon: {c['canon']}.")
    for s in PL["spaceport_sites"]:
        i, j = at(s["lon"], s["lat"])
        lines.append(f"- {'ok ' if land[i, j] else 'FAIL'} spaceport site {s['name']} ({s['status']}): {elev[i, j]:.0f} m")
    band = (g.LON >= 175) | (g.LON <= -175)
    rows = [i for i in range(g.H) if g.lat[i] >= 0]
    landrows = sum(1 for i in rows if land[i][band[i]].mean() > 0.5)
    lines.append(f"- Nemora band 175°E–175°W: {landrows / len(rows):.0%} of the rows from the equator to the pole are "
                 f"mostly land")
    i0 = int((90 - 40.5) / g.res)
    j0 = [j for j in range(g.W) if abs(abs(g.lon[j]) - 180) < 0.6]
    open_ = any(not land[i, j] for i in range(i0 - 3, i0 + 4) for j in j0)
    lines.append(f"- {'ok ' if open_ else 'FAIL'} Nemoran Strait open at 180°")
    for rg in PL["regions"]:
        x0, y0, x1, y1 = rg["box"]
        lo = np.where(g.LON < 0, g.LON + 360, g.LON) if x1 > 180 else g.LON
        m = (lo >= x0) & (lo <= x1) & (g.LAT >= y0) & (g.LAT <= y1)
        lines.append(f"- {rg['name']}: {land[m].mean():.0%} land, median {np.median(elev[m & land]):.0f} m. "
                     f"Canon: {rg['canon']}.")
    tot = (land * g.cell_km2).sum()
    lines.append(f"- Land (lakes included): {tot / 1e6:.1f}M km², {tot / (4 * math.pi * R_KM ** 2):.1%} of the surface")
    lab, n = ndimage.label(land, structure=np.ones((3, 3)))
    sizes = sorted(ndimage.sum(land * g.cell_km2, lab, index=np.arange(1, n + 1)))[::-1]
    lines.append("- Largest landmasses (M km², the date line splits B and D in this count): "
                 + ", ".join(f"{s / 1e6:.1f}" for s in sizes[:12]))
    return "\n".join(lines) + "\n"


# ----------------------------------------------------------------------------- output


def save_rasters(r):
    g = r["grid"]
    hm = np.clip(np.round(r["elev"] + 12000), 0, 65535).astype(np.uint16)
    Image.fromarray(hm).save(os.path.join(OUT, "heightmap.png"))
    Image.fromarray((r["land"] * 255).astype(np.uint8)).convert("1").save(os.path.join(OUT, "landmask.png"))
    meta = dict(projection="equirectangular; west edge 180°W, north edge 90°N", resolution_deg=g.res,
                size=[g.W, g.H], heightmap="16-bit greyscale PNG: elevation in metres = value - 12000 "
                "(the ice-sheet surface where there is ice; lake surfaces on lakes)",
                landmask="1-bit PNG: white = land (lakes count as land)")
    with open(os.path.join(OUT, "rasters.json"), "w", encoding="utf-8") as fh:
        json.dump(meta, fh, indent=2, ensure_ascii=False)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--res", type=float, default=0.1)
    ap.add_argument("--seed", type=int, default=7)
    ap.add_argument("--no-circulation", action="store_true")
    ap.add_argument("--no-render", action="store_true")
    a = ap.parse_args()
    os.makedirs(OUT, exist_ok=True)
    r = build(a.res, a.seed, set() if a.no_circulation else {"circulation"})
    text = checks(r)
    print(text)
    for name, st in r["probes"].items():
        print(f"  probe {name:14s} " + "  ".join(f"{k} {v:6.0f}" for k, v in st.items()))
    with open(os.path.join(OUT, "checks.md"), "w", encoding="utf-8") as fh:
        fh.write(text)
    save_rasters(r)
    if not a.no_render:
        import render
        render.all_maps(r, OUT)


if __name__ == "__main__":
    main()
