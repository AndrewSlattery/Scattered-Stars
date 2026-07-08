#!/usr/bin/env python3
"""Compile a curated subset of the lore for NotebookLM: enough grounding on
Arrhenos and the wider setting to reason well, without the procedural/
geographic detail (military doctrine, house genealogies, street-by-street
locations, conversion tables) that dwarfs the actual cultural content and
drowns it out in synthesis.

Companion to compile-lore.py, which compiles *everything*. This script is
deliberately narrower. Three output files, in reading order:

    notebooklm-0-orientation.md   Universal setting rules + historical/
                                   diplomatic backdrop (README, setting/,
                                   two appendices)
    notebooklm-1-arrhenos.md      Every top-level Arrhenos document (society,
                                   government, economy, culture, diaspora,
                                   external relations, the Banking War, etc.)
                                   plus a hand-picked slice of locations/:
                                   the regional index and the individual
                                   places that carry real social texture
                                   (market districts, sport, neighbourhoods,
                                   frontier cities, festivals, off-world
                                   holdings), skipping only the handful of
                                   one-paragraph infrastructure placeholders
                                   (university campus, transit hub, industrial
                                   district) that are explicitly marked
                                   "to be expanded" and carry no cultural
                                   content yet.
    notebooklm-2-wider-powers.md  Deliberately thin: just each power's
                                   culture.md (or nearest equivalent), plus
                                   the cross-power index and one concrete
                                   Drift Communities anchor. This is
                                   *context* for Arrhenos, not a subject in
                                   its own right, so it should read
                                   noticeably shorter than the Arrhenos file
                                   -- not longer.

Generated files -- do not edit by hand. Re-run after lore changes.
"""

from pathlib import Path

ROOT = Path(__file__).resolve().parent
README = ROOT / "README.md"


def walk_directory(directory, exclude=frozenset()):
    """Yield .md files from `directory` in logical order: index.md first, then
    the other files alphabetically, then subdirectories alphabetically
    (recursive). Any directory in `exclude` is skipped entirely."""
    if directory in exclude:
        return
    files = sorted(p for p in directory.iterdir() if p.is_file() and p.suffix == ".md")
    subdirs = sorted(p for p in directory.iterdir() if p.is_dir() and p not in exclude)

    index_file = next((f for f in files if f.name == "index.md"), None)
    other_files = [f for f in files if f.name != "index.md"]

    if index_file:
        yield index_file
    yield from other_files
    for sub in subdirs:
        yield from walk_directory(sub, exclude)


def render(files):
    """Render source files into concatenated, labelled markdown blocks."""
    parts = []
    for path in files:
        rel = path.relative_to(ROOT).as_posix()
        parts.append(f"<!-- source: {rel} -->")
        parts.append(f"## `{rel}`")
        parts.append("")
        parts.append(path.read_text(encoding="utf-8").rstrip())
        parts.append("")
        parts.append("---")
        parts.append("")
    return parts


def orientation_files():
    files = [README]
    files.extend(walk_directory(ROOT / "setting"))
    files.append(ROOT / "appendices" / "timeline.md")
    files.append(ROOT / "appendices" / "diplomatic-protocols.md")
    return [f for f in files if f.exists()]


def arrhenos_files():
    exclude = {ROOT / "worlds/arrhenos/locations", ROOT / "worlds/arrhenos/vessels"}
    files = list(walk_directory(ROOT / "worlds/arrhenos", exclude))
    files.extend(arrhenos_location_files())
    return files


def arrhenos_location_files():
    """Hand-picked slice of worlds/arrhenos/locations/: the regional index,
    every place with real social texture, and the off-world/orbital notes
    that round out Arrhenos's economic reach. Skips only the genuinely thin
    infrastructure stubs (transit hub, industrial district, university --
    each a single generic paragraph explicitly marked "to be expanded" with
    no cultural content yet)."""
    loc = ROOT / "worlds/arrhenos/locations"
    relative_paths = [
        "index.md",
        "campottoni.md",  # the capital, the Endeavour Fleet's landing site
        "landwick/index.md",  # coastal cultural centre
        "landwick/the-tep.md",  # squatter-turned-artist quarter, strong identity
        "brovdingonai/index.md",
        "brovdingonai/shambles.md",  # unplanned market district, the city's social heart
        "brovdingonai/stadium.md",  # jockey sport, spectator culture
        "brovdingonai/westslope-gardens.md",  # residential neighbourhood life
        "brovdingonai/fountain-plazas.md",  # civic wayfinding + the Carnival synchronisation
        "brovdingonai/nightlife.md",  # "comfortable rather than wild" -- a real cultural note
        "nemora-zespol/index.md",  # the great wilderness band
        "nemora-zespol/zespol.md",  # frontier research city grown up around it
        "verenstad-gamma/index.md",  # equatorial spaceport + orbital, tether economics
        "verenstad-gamma/verenstad.md",
        "verenstad-gamma/gamma.md",
        "verenstad-gamma/transient-quarter.md",  # spacers and stopovers, a liminal community
        "other.md",  # orbital financial stations, off-world holdings, minor settlements
    ]
    return [loc / rel for rel in relative_paths if (loc / rel).exists()]


def wider_powers_files():
    # Deliberately thin: the cross-power index, then each power's culture
    # document alone (not index.md/government/military). This is context for
    # Arrhenos, not a subject in its own right.
    files = [ROOT / "powers/index.md"]
    culture_files = [
        "drift-communities/overview.md",  # stateless; overview.md is their culture-equivalent
        "drift-communities/haven-ascendant/index.md",  # one concrete community, for grounding
        "elysian-collective/culture.md",
        "mandate/culture.md",
        "neo-solar-republic/culture.md",
        "sable-cartel/culture.md",
        "union-freeholds/culture.md",
        "vega-throne/culture.md",
    ]
    files.extend(ROOT / "powers" / rel for rel in culture_files)
    return [f for f in files if f.exists()]


SECTIONS = [
    {"output": "notebooklm-0-orientation.md", "title": "Orientation", "collect": orientation_files},
    {"output": "notebooklm-1-arrhenos.md", "title": "Arrhenos", "collect": arrhenos_files},
    {"output": "notebooklm-2-wider-powers.md", "title": "The Wider Powers (context)", "collect": wider_powers_files},
]


def compile_section(section):
    sources = section["collect"]()
    header = [
        f"# Scattered Stars -- {section['title']}",
        "",
        f"_Curated for NotebookLM. Auto-generated from {len(sources)} source files. Do not edit directly._",
        "",
        "---",
        "",
    ]
    output = ROOT / section["output"]
    output.write_text("\n".join(header + render(sources)), encoding="utf-8")
    print(f"Wrote {section['output']:<28} from {len(sources):>2} files ({output.stat().st_size:>7,} bytes).")


def compile_lore_notebooklm():
    for section in SECTIONS:
        compile_section(section)


if __name__ == "__main__":
    compile_lore_notebooklm()
