"""Copy tutorial sources to a NEW directory without Git history or local state."""

import argparse
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FILES = (
    "README.md", "LICENSE", ".gitignore", ".gitattributes", "pyproject.toml",
    "uv.lock", "params.json", "dvc.yaml", "scripts/make_data.py",
    "scripts/train.py", "scripts/create_lab.py", "tests/test_example.py",
)


def create_lab(destination: Path) -> Path:
    destination = destination.resolve()
    if destination == ROOT or ROOT in destination.parents:
        raise ValueError("Choose a directory outside this repository.")
    # exist_ok=False also protects an existing empty folder from being modified.
    destination.mkdir(parents=True, exist_ok=False)
    sources = [ROOT / name for name in FILES] + sorted((ROOT / "docs").glob("*.md"))
    for source in sources:
        target = destination / source.relative_to(ROOT)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
    return destination


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("destination", type=Path)
    args = parser.parse_args()
    try:
        destination = create_lab(args.destination)
    except (ValueError, FileExistsError) as error:
        parser.exit(1, f"Cannot create lab: {error}\n")
    print(f"Created lab at {destination}")
    print("Next: enter the new directory and continue lab step 1 at 'git init -b main'.")


if __name__ == "__main__":
    main()
