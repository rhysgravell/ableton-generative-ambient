#!/usr/bin/env python3
"""
Buried Landscapes — Ableton Project Organizer

Puts each .als file in a folder into its own named subfolder with standard
subfolders inside. Python version of the bash snippet in the project docs.

Created subfolders per project:
  <name>/
  ├── Samples/
  │   ├── Recorded/
  │   ├── Imported/
  │   └── Bounces/
  └── Versions/

Usage:
  python3 scripts/organize_project.py ~/Ableton/Buried_Landscapes/Ideas
  python3 scripts/organize_project.py ~/Ableton/Buried_Landscapes/Ideas --dry-run
"""

import argparse
import shutil
from pathlib import Path


SUBFOLDERS = [
    "Samples/Recorded",
    "Samples/Imported",
    "Samples/Bounces",
    "Versions",
]


def organize(folder: Path, dry_run: bool = False) -> None:
    als_files = sorted(folder.glob("*.als"))
    if not als_files:
        print(f"No .als files found in {folder}")
        return

    prefix = "DRY RUN — " if dry_run else ""
    print(f"{prefix}Organizing {len(als_files)} project(s) in {folder}\n")

    for als in als_files:
        dest_folder = folder / als.stem
        print(f"  {als.name}")
        print(f"    → {dest_folder.relative_to(folder)}/")
        for sub in SUBFOLDERS:
            print(f"       {dest_folder.relative_to(folder)}/{sub}/")

        if not dry_run:
            for sub in SUBFOLDERS:
                (dest_folder / sub).mkdir(parents=True, exist_ok=True)
            shutil.move(str(als), dest_folder / als.name)
        print()

    if dry_run:
        print("(dry run — no files moved. Re-run without --dry-run to apply.)")
    else:
        print(f"Done! {len(als_files)} project(s) organized.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Buried Landscapes — Organize Ableton Ideas folder",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Examples:\n"
               "  python3 scripts/organize_project.py ~/Ableton/Buried_Landscapes/Ideas\n"
               "  python3 scripts/organize_project.py ~/Ableton/Buried_Landscapes/Ideas --dry-run\n",
    )
    parser.add_argument("folder", help="Folder containing .als files to organize")
    parser.add_argument("--dry-run", action="store_true",
                        help="Preview what would happen without moving any files")
    args = parser.parse_args()

    folder = Path(args.folder).expanduser().resolve()
    if not folder.is_dir():
        print(f"Error: not a directory: {folder}")
        raise SystemExit(1)

    organize(folder, dry_run=args.dry_run)
