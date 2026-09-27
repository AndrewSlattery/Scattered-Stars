# Arrhenos sketch map: how it works

The sketch is built from four small, hand-editable JSON layers. A script turns them into a heightmap, a land mask, a set of maps, a simple wind and ocean-current model, and a list of canon checks. The reasoning behind the physical choices is in [../physical-model.md](../physical-model.md); the decisions it rests on are in [../decisions.md](../decisions.md).

## Layers

| landmasses.json | Outlines. `land` polygons are unioned, then `water` polygons (seas, straits, lakes) are cut out. Straits are always kept open in full. Seas and lakes keep an always-open core about 35 km inside their edge, and their shores get the same irregularity as any coast. Small islands carry a `kind` and are added back after the cut, so they can sit inside a sea. |
| tectonics.json  | Plates (labels only), boundaries as polylines with a `kind` (ridge, rift, trench, transform, suture, failed-rift), and hotspots with their tracks. Trenches say which side overrides. |
| relief.json     | Mountain ranges (polylines with height, half-width and style), volcanoes, plateaus, lowland basins, the ice sheet's margin, and coast zones that set the character of a stretch of coast (fjord, skerry, smooth, rift, strait, tidal, inland, delta). |
| places.json     | Canon cities and regions, and the seven equatorial spaceport sites. Used for labels and checks, and to keep canon places where the text puts them: every place is guaranteed to be on land, and cities marked `coastal` stay on the coast. |

Coordinates are `[lon, lat]` in degrees. Within any one polygon or line, longitudes run continuously and may pass ±180 (D, for example, is drawn from 148 to 201). B covers the north pole by running its outline along latitude 90.

B and B·nw both overlap into the Rift Sea and are cut apart by the Rift Sea polygon. If you move the Rift Sea, keep it covering both of their edges, or the two continents will join up again.

## Building

```bash
pip install -r requirements.txt
```

```bash
python build_sketch.py --res 0.25
```

That makes a quick draft (about two minutes). Leave out `--res` for the full 0.1° build (about fifteen minutes). `--seed` changes the random detail (coastline wiggles, peaks, seamounts) without moving anything the layers specify.

## Outputs (out/)

| sketch.png            | The plain outline map: coasts, names, canon places, proposed spaceport sites |
| physical-labelled.png | Shaded relief with labels |
| physical.jpg          | Shaded relief, full resolution, no labels |
| tectonics.png         | Plates, boundaries, hotspots |
| winds.png             | Idealised prevailing winds |
| currents.png          | Wind-driven surface currents from the ocean model; red flows poleward (warm), blue toward the equator (cold) |
| coasts.png            | Coast character inferred from latitude, prevailing wind, current and relief |
| heightmap.png         | 16-bit greyscale, equirectangular from 180°W: elevation in metres = value − 12000 |
| landmask.png          | 1-bit land mask, same grid |
| checks.md             | Whether each canon place came out where it should, and land statistics |

## Limits

This is a sketch, not a simulation. Relief is procedural: ranges, plateaus and basins placed by hand and textured with noise. There is no erosion or river network yet. The winds are an idealised annual mean. The currents come from a steady, depth-averaged, wind-driven (Stommel) model with the island rule on a 1° grid, which captures the gyres, the western boundary currents and the main warm and cold coasts, but not density-driven flow, seasons or monsoons. The coast classification is a rule of thumb built on those two.
