"""Remove non-font files from unzipped-fonts using inventory-before.csv."""

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FONT_EXTENSIONS = {".otf", ".ttf", ".woff", ".woff2", ".otc", ".ttc", ".eot"}
BEFORE = ROOT / "inventory-before.csv"


def main() -> None:
    rows = list(csv.DictReader(BEFORE.open(encoding="utf-8-sig")))
    removed = 0
    missing = 0
    for row in rows:
        if row["kind"] != "other":
            continue
        path = ROOT / row["path"]
        if path.is_file():
            path.unlink()
            removed += 1
        else:
            missing += 1
    empty = 0
    for directory in sorted(
        (ROOT / "unzipped-fonts").rglob("*"),
        key=lambda item: len(item.parts),
        reverse=True,
    ):
        if directory.is_dir() and not any(directory.iterdir()):
            directory.rmdir()
            empty += 1
    print(f"removed={removed} missing={missing} empty_dirs={empty}")


if __name__ == "__main__":
    main()
