"""Map renders for the Arrhenos sketch (called from build_sketch.py)."""
import math, os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap, TwoSlopeNorm
from matplotlib import patheffects as pe
from PIL import Image

CENTRE = 120.0
X0, X1 = CENTRE - 180, CENTRE + 180
EXTENT = (X0, X1, -90, 90)
HALO = [pe.withStroke(linewidth=2.6, foreground="white")]
DARK_HALO = [pe.withStroke(linewidth=2.2, foreground=(0.08, 0.12, 0.2, 0.8))]


def recenter(a, res):
    return np.roll(a, -int(round((X0 + 180) / res)), axis=1)


def frame_lon(lon):
    return (np.asarray(lon, float) - X0) % 360 + X0


def interp_rgb(x, stops):
    xs = [s[0] for s in stops]
    return np.stack([np.interp(x, xs, [s[1][k] for s in stops]) for k in range(3)], -1) / 255.0


LAND_STOPS = [(0, (92, 142, 80)), (250, (118, 158, 88)), (550, (150, 170, 102)), (950, (180, 174, 116)),
              (1450, (176, 150, 108)), (2050, (156, 126, 96)), (2800, (138, 118, 104)), (3600, (166, 160, 154)),
              (4400, (218, 216, 214)), (5400, (250, 250, 250))]
SEA_STOPS = [(-6000, (26, 62, 112)), (-4500, (36, 84, 140)), (-3000, (56, 112, 168)), (-1200, (92, 150, 196)),
             (-200, (128, 182, 214)), (0, (160, 205, 226))]


def hillshade(elev, lat, res, exag=18.0, az=315, alt=40):
    """Lambertian shading; light from the north-west by default."""
    dy = 6371e3 * math.radians(res)
    dx = dy * np.maximum(np.cos(np.radians(lat)), 0.05)[:, None]
    gy = -np.gradient(elev, dy, axis=0)  # rows run north to south; make +y point north
    gx = (np.roll(elev, -1, 1) - np.roll(elev, 1, 1)) / (2 * dx)
    nx, ny, nz = -exag * gx, -exag * gy, np.ones_like(elev)
    norm = np.sqrt(nx * nx + ny * ny + nz * nz)
    azr, altr = math.radians(az), math.radians(alt)
    lx, ly, lz = math.sin(azr) * math.cos(altr), math.cos(azr) * math.cos(altr), math.sin(altr)
    return np.clip((nx * lx + ny * ly + nz * lz) / norm, 0, 1)


def physical_rgb(r):
    g, e, land, ice = r["grid"], r["elev"], r["land"], r["ice"]
    lat = g.LAT
    snowline = 5200 * np.clip(np.cos(np.radians(lat)), 0, 1) ** 1.7 + 300
    rgb = np.where(land[..., None], interp_rgb(e, LAND_STOPS), interp_rgb(e, SEA_STOPS))
    snow = land & (e > snowline)
    rgb[snow] = rgb[snow] * 0.3 + 0.7 * np.array([0.96, 0.96, 0.97])
    rgb[ice] = np.array([0.93, 0.95, 0.98])
    rgb[r["lake"]] = np.array([0.45, 0.66, 0.82])
    sh = hillshade(e, g.lat, g.res)
    k = np.where(land & ~r["lake"], 0.45 + 0.75 * sh, 0.88 + 0.2 * sh)[..., None]
    return np.clip(rgb * k, 0, 1)


def base_axes(figw=24, title=None):
    fig = plt.figure(figsize=(figw, figw / 2 + 0.6), dpi=120)
    ax = fig.add_axes([0.01, 0.01, 0.98, 0.98 * (figw / 2) / (figw / 2 + 0.6)])
    ax.set_xlim(X0, X1); ax.set_ylim(-90, 90); ax.set_aspect("equal"); ax.axis("off")
    if title:
        fig.text(0.012, 0.985, title, fontsize=15, weight="bold", va="top", color="#222")
    return fig, ax


def graticule(ax, color="#ffffff", alpha=0.35, labels=True):
    for lo in range(-60, 301, 30):
        ax.axvline(lo, color=color, lw=0.6, alpha=alpha, zorder=2)
        if labels and X0 <= lo < X1:
            l = (lo + 180) % 360 - 180
            ax.text(lo + 1, 88, f"{abs(l)}°{'E' if l > 0 else 'W' if l < 0 else ''}", fontsize=8, color="#333",
                    va="top", path_effects=HALO, zorder=9)
    for la in range(-60, 61, 30):
        ax.axhline(la, color=color, lw=0.6 if la else 1.0, alpha=alpha, zorder=2)
        if labels:
            ax.text(X0 + 1, la + 1, f"{abs(la)}°{'N' if la > 0 else 'S' if la < 0 else ''}", fontsize=8, color="#333",
                    path_effects=HALO, zorder=9)


def coast(ax, lon, lat, mask, **kw):
    """Coastline contour; lat may run north to south."""
    ax.contour(lon, lat[::-1], np.asarray(mask, float)[::-1], levels=[0.5], **kw)


def plot_line(ax, line, **kw):
    ln = np.array(line, float)
    lon = np.unwrap(np.radians(ln[:, 0]))
    lon = np.degrees(lon)
    base = frame_lon(lon[0]) - lon[0]
    for off in (-360, 0, 360):
        ax.plot(lon + base + off, ln[:, 1], **kw)


def text_at(ax, lon, lat, s, **kw):
    ax.text(frame_lon(lon), lat, s, **kw)


def cities(ax, PL, small=False):
    for c in PL["cities"]:
        x = frame_lon(c["lon"])
        ax.plot(x, c["lat"], "o", ms=5 if small else 6, mfc="#c62828", mec="white", mew=1.2, zorder=10)
        ax.text(x + 1.2, c["lat"] + 0.8, c["name"], fontsize=8.5 if small else 9.5, color="#7a1010", weight="bold",
                path_effects=HALO, zorder=10)


def save(fig, path):
    fig.savefig(path, dpi=120)
    plt.close(fig)
    im = Image.open(path).convert("RGB")
    im.quantize(colors=256, method=Image.Quantize.FASTOCTREE, dither=Image.Dither.NONE).save(path, optimize=True) \
        if path.endswith("sketch.png") or path.endswith("tectonics.png") else im.save(path, optimize=True)


# ----------------------------------------------------------------------------- the maps


def physical(r, out):
    g = r["grid"]
    rgb = physical_rgb(r)
    img = (recenter(rgb, g.res) * 255).astype(np.uint8)
    Image.fromarray(img).save(os.path.join(out, "physical.jpg"), quality=90)
    fig, ax = base_axes(24, "Arrhenos — physical sketch (v1)")
    ax.imshow(recenter(rgb, g.res), extent=EXTENT, interpolation="lanczos", zorder=1)
    graticule(ax)
    labels(ax, r, physical=True)
    cities(ax, r["PL"], small=True)
    save(fig, os.path.join(out, "physical-labelled.png"))


def labels(ax, r, physical=False):
    for f in r["L"]["land"]:
        if f.get("label") and f["id"] not in ("H1", "H2"):
            text_at(ax, f["label"][0], f["label"][1], f["name"].split(" — ")[0], fontsize=26 if len(f["id"]) <= 3 else 20,
                    weight="bold", color="#1b2a4a", ha="center", va="center", alpha=0.85, path_effects=HALO, zorder=8)
    text_at(ax, -141.5, -5.5, "H", fontsize=20, weight="bold", color="#1b2a4a", ha="center", path_effects=HALO, zorder=8)
    for w in r["L"]["water"]:
        if w.get("label") and w["kind"] in ("sea", "lake") and "basin" not in w["name"] and "arm" not in w["name"]:
            text_at(ax, w["label"][0], w["label"][1], w["name"], fontsize=9, style="italic", color="#0d3b66",
                    ha="center", rotation=90 if w["id"] == "rift-sea" else 0, path_effects=HALO, zorder=8)
    extra = [(-10, -22.5, "Campottonì Gulf", -18), (-30, 44.6, "inland sea", 0), (97, 38, "back-arc gulf", 0),
             (180, 43.2, "Nemoran Strait", 0), (-104, 43, "delta gulf", 0)]
    for lo, la, s, rot in extra:
        text_at(ax, lo, la, s, fontsize=8.5, style="italic", color="#0d3b66", ha="center", rotation=rot,
                path_effects=HALO, zorder=8)
    seas = [(-50, 22, "Western Ocean"), (60, -2, "Central Ocean"), (52, 55, "Northern Sea"), (-20, 72, "Polar Sea"),
            (160, -35, "Southern Ocean"), (-152, 16, "Northeast Ocean"), (0, -68, "Austral Sea")]
    for lo, la, s in seas:
        text_at(ax, lo, la, s, fontsize=13, style="italic", color="#2b5d8a", ha="center", alpha=0.9,
                path_effects=HALO, zorder=7)


def sketch(r, out):
    """The plain outline map: coasts, names, canon places."""
    g, PL = r["grid"], r["PL"]
    land = recenter(r["land"].astype(float), g.res)
    ice = recenter(r["ice"].astype(float), g.res)
    lake = recenter(r["lake"].astype(float), g.res)
    fig, ax = base_axes(24, "Arrhenos — sketch map v1: outlines")
    base = np.where(land[..., None] > 0.5, np.array([0.95, 0.92, 0.84]), np.array([0.80, 0.89, 0.94]))
    base = np.where((ice[..., None] > 0.5) & (land[..., None] > 0.5), np.array([0.97, 0.98, 1.0]), base)
    base = np.where(lake[..., None] > 0.5, np.array([0.70, 0.84, 0.92]), base)
    ax.imshow(base, extent=EXTENT, interpolation="nearest", zorder=1)
    lon = np.linspace(X0 + g.res / 2, X1 - g.res / 2, g.W)
    coast(ax, lon, g.lat, (land > 0.5) & (lake < 0.5), colors="#4a3b2a", linewidths=0.7, zorder=3)
    graticule(ax, color="#7a8a99", alpha=0.35)
    for rg in PL["regions"]:
        x0, y0, x1, y1 = rg["box"]
        xs = frame_lon(x0)
        ax.add_patch(plt.Rectangle((xs, y0), x1 - x0, y1 - y0, fill=False, ec="#9a6a00", lw=1.2, ls="--", zorder=6))
        ax.text(xs + (x1 - x0) / 2, y0 - 2.2 if rg["name"] != "Nemora" else 3, rg["name"], fontsize=8.5,
                color="#8a5a00", ha="center", weight="bold", path_effects=HALO, zorder=9)
    for s in PL["spaceport_sites"]:
        ax.plot(frame_lon(s["lon"]), s["lat"], marker="^", ms=8, mfc="#6a1b9a" if s["status"] == "proposed" else "#c62828",
                mec="white", mew=1, zorder=11)
    labels(ax, r)
    cities(ax, PL)
    ax.plot([], [], "^", mfc="#6a1b9a", mec="white", ms=8, label="proposed equatorial spaceport site")
    ax.plot([], [], "o", mfc="#c62828", mec="white", ms=6, label="canon city")
    ax.legend(loc="lower left", fontsize=9, framealpha=0.9)
    save(fig, os.path.join(out, "sketch.png"))


KIND_STYLE = dict(ridge=dict(color="#d62728", lw=2.2), rift=dict(color="#ff7f0e", lw=2.4),
                  transform=dict(color="#2ca02c", lw=1.8), trench=dict(color="#1f3a93", lw=2.0),
                  suture=dict(color="#8c6d31", lw=1.4, ls=(0, (4, 3))),
                  **{"failed-rift": dict(color="#b15928", lw=1.6, ls=(0, (2, 2)))})


def tectonics(r, out):
    g, T = r["grid"], r["T"]
    e = recenter(r["elev"], g.res)
    land = recenter(r["land"], g.res)
    fig, ax = base_axes(24, "Arrhenos — plates, boundaries and hotspots (sketch v1)")
    img = np.where(land[..., None], np.array([0.86, 0.84, 0.80]), interp_rgb(e, SEA_STOPS) * 0.35 + 0.63)
    ax.imshow(img, extent=EXTENT, interpolation="lanczos", zorder=1)
    lon = np.linspace(X0 + g.res / 2, X1 - g.res / 2, g.W)
    coast(ax, lon, g.lat, land, colors="#6b5d4f", linewidths=0.5, zorder=2)
    graticule(ax, color="#777", alpha=0.25)
    for b in T["boundaries"]:
        st = KIND_STYLE[b["kind"]]
        plot_line(ax, b["line"], zorder=5, solid_capstyle="round", **st)
        if b["kind"] == "trench":
            teeth(ax, b["line"], b.get("over", "left"), st["color"])
    for p in T["plates"]:
        x, y = frame_lon(p["label"][0]), p["label"][1]
        ax.text(x, y, p["name"], fontsize=12, style="italic", weight="bold", color="#3a2f63", ha="center",
                path_effects=HALO, zorder=9)
        if p["id"] == "austral":
            mx, my = p["motion"]
            ax.annotate("", xy=(x + 7 * mx, y - 3 + 7 * my), xytext=(x, y - 3),
                        arrowprops=dict(arrowstyle="-|>", color="#3a2f63", lw=2.2), zorder=9)
            ax.text(x + 2, y - 7, "drifting south over the Landwick hotspot", fontsize=8.5, color="#3a2f63",
                    path_effects=HALO, zorder=9)
    for h in T["hotspots"]:
        tr = np.array(h["track"])
        plot_line(ax, h["track"], color="#e377c2", lw=1.6, ls=":", zorder=6)
        ax.plot(frame_lon(h["now"][0]), h["now"][1], marker="*", ms=16, mfc="#e377c2", mec="white", zorder=10)
        ax.text(frame_lon(h["now"][0]) + 2, h["now"][1] + 1, h["name"], fontsize=9, color="#9c2a7b",
                path_effects=HALO, zorder=10)
    for kind, lab in [("ridge", "spreading ridge"), ("rift", "young rift"), ("trench", "subduction (teeth on the overriding side)"),
                      ("transform", "transform fault"), ("suture", "old suture / orogen"), ("failed-rift", "failed rift")]:
        ax.plot([], [], label=lab, **KIND_STYLE[kind])
    ax.plot([], [], "*", ms=12, mfc="#e377c2", mec="white", label="hotspot (dotted: track)")
    ax.legend(loc="lower left", fontsize=10, framealpha=0.92)
    cities(ax, r["PL"], small=True)
    save(fig, os.path.join(out, "tectonics.png"))


def teeth(ax, line, over, color):
    ln = np.array(line, float)
    ln[:, 0] = np.degrees(np.unwrap(np.radians(ln[:, 0])))
    seg = np.diff(ln, axis=0)
    L = np.hypot(seg[:, 0], seg[:, 1])
    pos = np.arange(1.5, L.sum(), 3.2)
    cum = np.concatenate([[0], np.cumsum(L)])
    base = frame_lon(ln[0, 0]) - ln[0, 0]
    for s in pos:
        k = np.searchsorted(cum, s) - 1
        t = (s - cum[k]) / L[k]
        p = ln[k] + t * seg[k]
        d = seg[k] / L[k]
        n = np.array([-d[1], d[0]]) * (1 if over == "left" else -1)
        tri = np.array([p - 0.9 * d, p + 0.9 * d, p + 1.4 * n])
        for off in (-360, 0, 360):
            ax.fill(tri[:, 0] + base + off, tri[:, 1], color=color, zorder=5, lw=0)


def winds(r, out):
    from build_sketch import wind_profile, HADLEY, POLAR_FRONT
    g = r["grid"]
    land = recenter(r["land"], g.res)
    fig, ax = base_axes(24, "Arrhenos — prevailing surface winds (idealised annual mean, sketch v1)")
    img = np.where(land[..., None], np.array([0.88, 0.86, 0.80]), np.array([0.86, 0.92, 0.96]))
    ax.imshow(img, extent=EXTENT, interpolation="nearest", zorder=1)
    for la0, la1, c, name in [(-HADLEY, HADLEY, "#f6c85f", "trade winds (easterlies)"),
                              (HADLEY, POLAR_FRONT, "#9dd9a3", "westerlies"),
                              (-POLAR_FRONT, -HADLEY, "#9dd9a3", None),
                              (POLAR_FRONT, 90, "#b8c7e6", "polar easterlies"),
                              (-90, -POLAR_FRONT, "#b8c7e6", None)]:
        ax.axhspan(la0, la1, color=c, alpha=0.18, zorder=1.5, label=name)
    lon = np.linspace(X0 + g.res / 2, X1 - g.res / 2, g.W)
    coast(ax, lon, g.lat, land, colors="#6b5d4f", linewidths=0.6, zorder=2)
    lo = np.arange(X0 + 4, X1, 8.0); la = np.arange(-84, 85, 6.0)
    LO, LA = np.meshgrid(lo, la)
    u, v = wind_profile(LA)
    ax.quiver(LO, LA, u, v, color="#34495e", scale=260, width=0.0016, zorder=4)
    for y, s in [(0, "ITCZ (doldrums): rising air, heavy rain"), (HADLEY, "subtropical highs: deserts"),
                 (-HADLEY, "subtropical highs: deserts"), (POLAR_FRONT, "polar front: storm track"),
                 (-POLAR_FRONT, "polar front: storm track")]:
        ax.axhline(y, color="#555", lw=1, ls="--", zorder=3)
        ax.text(X0 + 2, y + 0.8, s, fontsize=9, color="#333", path_effects=HALO, zorder=9)
    graticule(ax, color="#777", alpha=0.2)
    ax.legend(loc="lower right", fontsize=10, framealpha=0.92)
    save(fig, os.path.join(out, "winds.png"))


def currents(r, out):
    c = r.get("circ")
    if c is None:
        return
    g = r["grid"]
    land = recenter(r["land"], g.res)
    fig, ax = base_axes(24, "Arrhenos — wind-driven surface currents (Stommel model, sketch v1)")
    img = np.where(land[..., None], np.array([0.90, 0.88, 0.82]), np.array([0.90, 0.94, 0.97]))
    ax.imshow(img, extent=EXTENT, interpolation="nearest", zorder=1)
    lon = np.linspace(X0 + g.res / 2, X1 - g.res / 2, g.W)
    coast(ax, lon, g.lat, land, colors="#6b5d4f", linewidths=0.6, zorder=2)
    res1 = 360 / c["U"].shape[1]
    U, V = recenter(c["U"], res1), recenter(c["V"], res1)
    oc = recenter(c["ocean"], res1)
    lat = c["lat"][::-1]
    U, V, oc = U[::-1], V[::-1], oc[::-1]
    lo1 = np.linspace(X0 + res1 / 2, X1 - res1 / 2, U.shape[1])
    spd = np.hypot(U, V)
    warmth = np.sign(lat)[:, None] * V / (spd + 1e-9)  # + poleward (warm), - equatorward (cold)
    warmth = np.where(oc, warmth, np.nan)
    Um, Vm = np.ma.masked_where(~oc, U), np.ma.masked_where(~oc, V)
    warmth = np.ma.masked_invalid(warmth)
    lw = 0.5 + 3.0 * np.clip(spd / np.nanpercentile(spd[oc], 97), 0, 1)
    cmap = LinearSegmentedColormap.from_list("wc", ["#1f5fbf", "#8fa3b8", "#d7301f"])
    strm = ax.streamplot(lo1, lat, Um, Vm, color=warmth, cmap=cmap, norm=TwoSlopeNorm(0, -1, 1), linewidth=lw,
                         density=4.2, arrowsize=0.9, zorder=4)
    graticule(ax, color="#777", alpha=0.2)
    cb = fig.colorbar(strm.lines, ax=ax, orientation="horizontal", fraction=0.025, pad=0.01, aspect=60)
    cb.set_label("blue: flowing toward the equator (cold)    red: flowing toward the pole (warm)    width: strength")
    cities(ax, r["PL"], small=True)
    save(fig, os.path.join(out, "currents.png"))


COAST_CLASSES = [
    ("ice", "#8fd3ff", "ice coast: ice cliffs, sea ice much of the year"),
    ("fjord", "#7b3294", "fjords and skerries: glacier-cut, mountain-backed, windward"),
    ("rift", "#e66101", "rift coast: straight, steep, young; narrow shelf"),
    ("tidal", "#e7298a", "tidal gulf: shallow, mudflats and salt marsh, big tides, tidal bores"),
    ("inland", "#35978f", "brackish inland sea: small tides, skerries, winter ice in the north"),
    ("delta", "#1a9850", "delta and marsh: big rivers, brackish flats"),
    ("desert", "#c9a227", "cold-current desert coast: fog, dunes, upwelling fisheries"),
    ("warm", "#d7301f", "warm-current coast: humid, long beaches, barrier islands, lagoons"),
    ("equatorial", "#66bd63", "equatorial coast: rain all year, swampy shores (mangroves only where planted)"),
    ("storm", "#2166ac", "windward storm coast: cliffs, heavy swell, gales"),
    ("lee", "#a6761d", "sheltered lee coast: drier, calmer water"),
    ("temperate", "#9e9e9e", "mixed temperate coast"),
]


def coast_classes(r):
    """Classify coastal cells (at ~0.25°) from latitude, facing, prevailing wind, current and relief."""
    from scipy import ndimage
    from build_sketch import wind_profile
    g, c = r["grid"], r.get("circ")
    k = max(1, int(round(0.25 / g.res)))
    H, W = g.H // k, g.W // k
    pool = lambda a, f: getattr(a[:H * k, :W * k].reshape(H, k, W, k), f)((1, 3))
    land = pool(r["land"].astype(float), "mean") > 0.5
    elev = pool(r["elev"], "max")
    ice = pool(r["ice"].astype(float), "mean") > 0.3
    zone = {s: pool(v, "mean") for s, v in r["zone"].items()}
    lat = 90 - (np.arange(H) + 0.5) * (180 / H)
    LAT = np.repeat(lat[:, None], W, 1)
    sea = ~land
    nb = np.zeros_like(land)
    nb[1:] |= sea[:-1]; nb[:-1] |= sea[1:]; nb |= np.roll(sea, 1, 1); nb |= np.roll(sea, -1, 1)
    coastal = land & nb
    lf = ndimage.gaussian_filter(land.astype(float), 2.5, mode=("nearest", "wrap"))
    gy = -np.gradient(lf, axis=0)
    gx = (np.roll(lf, -1, 1) - np.roll(lf, 1, 1)) / 2 / np.maximum(np.cos(np.radians(LAT)), 0.1)
    nx, ny = -gx, -gy
    nn = np.hypot(nx, ny) + 1e-9
    nx, ny = nx / nn, ny / nn
    u, v = wind_profile(LAT)
    onshore = -(u * nx + v * ny) / (np.hypot(u, v) + 1e-6)
    relief = ndimage.maximum_filter(elev, size=7, mode=("nearest", "wrap"))
    warm = np.zeros_like(elev)
    if c is not None:
        spd = np.hypot(c["U"], c["V"]) * c["ocean"]
        wm = np.sign(c["lat"])[:, None] * c["V"] * c["ocean"]
        num = ndimage.uniform_filter(wm, 5, mode=("nearest", "wrap"))
        den = ndimage.uniform_filter(spd, 5, mode=("nearest", "wrap")) + 1e-9
        w1 = num / den
        ri = np.clip(((90 - lat) / (180 / w1.shape[0])).astype(int), 0, w1.shape[0] - 1)
        ci = ((np.arange(W) + 0.5) * (w1.shape[1] / W)).astype(int)
        warm = w1[ri][:, ci]
    a = np.abs(LAT)
    cls = np.full(land.shape, "temperate", dtype=object)
    cls[(a < 10)] = "equatorial"
    cls[(a >= 34) & (a < 62) & (onshore < -0.2)] = "lee"
    cls[(a >= 38) & (a < 64) & (onshore > 0.25)] = "storm"
    cls[(a < 38) & (warm > 0.2) & (nx > -0.3)] = "warm"
    cls[(a >= 12) & (a <= 33) & (warm < -0.2) & (nx < 0.2)] = "desert"
    cls[zone["smooth"] > 0.5] = "desert"
    cls[zone["delta"] > 0.5] = "delta"
    cls[zone["inland"] > 0.5] = "inland"
    cls[zone["tidal"] > 0.5] = "tidal"
    cls[((a >= 42) & (onshore > 0.15) & (relief > 900)) | (zone["fjord"] > 0.5) | (zone["skerry"] > 0.5)] = "fjord"
    cls[(zone["rift"] > 0.5) | (zone["strait"] > 0.5)] = "rift"
    cls[ice | (a > 74)] = "ice"
    return coastal, cls, (H, W)


def coasts(r, out):
    from matplotlib.colors import to_rgba
    from scipy import ndimage
    coastal, cls, (H, W) = coast_classes(r)
    res = 180 / H
    land = recenter(r["land"], r["grid"].res)
    fig, ax = base_axes(24, "Arrhenos — coast character from winds, currents and relief (sketch v1)")
    img = np.where(land[..., None], np.array([0.93, 0.92, 0.89]), np.array([0.93, 0.96, 0.98]))
    ax.imshow(img, extent=EXTENT, interpolation="nearest", zorder=1)
    rgba = np.zeros((H, W, 4))
    for name, col, _ in COAST_CLASSES:
        m = ndimage.binary_dilation(coastal & (cls == name), iterations=1) & ~(rgba[..., 3] > 0)
        rgba[m] = to_rgba(col)
    ax.imshow(recenter(rgba, res), extent=EXTENT, interpolation="nearest", zorder=3)
    graticule(ax, color="#888", alpha=0.25)
    for name, col, lab in COAST_CLASSES:
        ax.plot([], [], color=col, lw=5, label=lab)
    ax.legend(loc="lower left", fontsize=9.5, framealpha=0.95)
    cities(ax, r["PL"], small=True)
    save(fig, os.path.join(out, "coasts.png"))


def all_maps(r, out):
    coasts(r, out)
    sketch(r, out)
    physical(r, out)
    tectonics(r, out)
    winds(r, out)
    currents(r, out)
