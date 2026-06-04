#!/usr/bin/env python3
"""Compile the lore .md files into a handful of numbered section files.

Instead of one giant LORE.md, this writes one file per major section at the
repo root:

    1-setting.md     setting/           (prefixed with README.md)
    2-powers.md      powers/
    3-world.md       worlds/            (minus worlds/arrhenos/)
    4-arrhenos.md    worlds/arrhenos/   (split out — it dwarfs the rest of worlds/)
    5-appendices.md  appendices/

Each file concatenates its source documents in a stable, readable order:
index.md first, then the remaining files alphabetically, then subdirectories
(applied recursively). The output files are generated — do not edit by hand.
"""

from pathlib import Path

ROOT = Path(__file__).resolve().parent
README = ROOT / "README.md"

# Each section becomes one output file. `roots` are walked in order; any path in
# `exclude` is skipped, which is how worlds/arrhenos is kept out of the world file
# and given its own. `readme` prepends README.md ahead of the section's content.
SECTIONS = [
    {"output": "1-setting.md",    "title": "Setting",    "roots": ["setting"],          "readme": True},
    {"output": "2-powers.md",     "title": "Powers",     "roots": ["powers"]},
    {"output": "3-world.md",      "title": "Worlds",     "roots": ["worlds"], "exclude": ["worlds/arrhenos"]},
    {"output": "4-arrhenos.md",   "title": "Arrhenos",   "roots": ["worlds/arrhenos"]},
    {"output": "5-appendices.md", "title": "Appendices", "roots": ["appendices"]},
]

OUTPUT_NAMES = {section["output"] for section in SECTIONS}


def walk_directory(directory, exclude=frozenset()):
    """Yield .md files from `directory` in logical order: index.md first, then the
    other files alphabetically, then subdirectories alphabetically (recursive).
    Any directory in `exclude` is skipped entirely."""
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


def collect_section_files(section):
    """Return the ordered list of source .md files for one section."""
    exclude = {ROOT / rel for rel in section.get("exclude", [])}
    files = []
    for root in section["roots"]:
        directory = ROOT / root
        if directory.is_dir():
            files.extend(walk_directory(directory, exclude))
    return files


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


def compile_section(section):
    """Write one section file and return the set of source files it consumed."""
    sources = []
    if section.get("readme") and README.exists():
        sources.append(README)
    sources.extend(collect_section_files(section))

    header = [
        f"# Scattered Stars — {section['title']}",
        "",
        f"_Auto-generated from {len(sources)} source files. Do not edit directly._",
        "",
        "---",
        "",
    ]

    output = ROOT / section["output"]
    output.write_text("\n".join(header + render(sources)), encoding="utf-8")
    print(f"Wrote {section['output']:<16} from {len(sources):>2} files ({output.stat().st_size:>7,} bytes).")
    return set(sources)


def warn_uncaptured(emitted):
    """Warn about any .md file under the repo that no section picked up, so new
    content is never silently dropped from the compiled output."""
    for path in ROOT.rglob("*.md"):
        rel = path.relative_to(ROOT)
        if any(part.startswith(".") for part in rel.parts):
            continue
        if rel.name in OUTPUT_NAMES:  # a generated file
            continue
        if path not in emitted:
            print(f"  ! not in any section: {rel.as_posix()}")


def compile_lore():
    emitted = set()
    for section in SECTIONS:
        emitted |= compile_section(section)
    warn_uncaptured(emitted)


if __name__ == "__main__":
    compile_lore()
