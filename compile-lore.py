#!/usr/bin/env python3
"""Concatenate all lore .md files into a single LORE.md in a logical order."""

from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "LORE.md"

# Top-level ordering: setup, then worldbuilding layers outwards, then reference.
TOP_LEVEL_ORDER = ["setting", "powers", "worlds", "appendices"]


def walk_directory(directory: Path):
    """Yield .md files from a directory in logical order:
    index.md first, then other files alphabetically, then subdirectories alphabetically."""
    files = sorted(p for p in directory.iterdir() if p.is_file() and p.suffix == ".md")
    subdirs = sorted(p for p in directory.iterdir() if p.is_dir())

    index_file = next((f for f in files if f.name == "index.md"), None)
    other_files = [f for f in files if f.name != "index.md"]

    if index_file:
        yield index_file
    yield from other_files
    for sub in subdirs:
        yield from walk_directory(sub)


def collect_files():
    ordered = []
    readme = ROOT / "README.md"
    if readme.exists():
        ordered.append(readme)

    for name in TOP_LEVEL_ORDER:
        directory = ROOT / name
        if directory.is_dir():
            ordered.extend(walk_directory(directory))

    # Catch any top-level dirs not in the manual list, so nothing is silently dropped.
    known = set(TOP_LEVEL_ORDER)
    for extra in sorted(p for p in ROOT.iterdir() if p.is_dir() and p.name not in known and not p.name.startswith(".")):
        ordered.extend(walk_directory(extra))

    return ordered


def compile_lore():
    files = collect_files()
    parts = [
        "# Scattered Stars — Consolidated Lore",
        "",
        f"_Auto-generated from {len(files)} source files. Do not edit directly._",
        "",
        "---",
        "",
    ]

    for path in files:
        rel = path.relative_to(ROOT).as_posix()
        parts.append(f"<!-- source: {rel} -->")
        parts.append(f"## `{rel}`")
        parts.append("")
        parts.append(path.read_text(encoding="utf-8").rstrip())
        parts.append("")
        parts.append("---")
        parts.append("")

    OUTPUT.write_text("\n".join(parts), encoding="utf-8")
    print(f"Wrote {OUTPUT.name} from {len(files)} files ({OUTPUT.stat().st_size:,} bytes).")


if __name__ == "__main__":
    compile_lore()
