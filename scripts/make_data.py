"""Generate two deterministic dataset versions without downloading anything."""

import argparse
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def make_data(output: Path, version: int) -> None:
    """Version 1 has 40 rows; version 2 adds 20 rows with a shifted target."""
    if version not in (1, 2):
        raise ValueError("Dataset version must be 1 or 2.")
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.writer(stream, lineterminator="\n")
        writer.writerow(["x", "y"])
        for index in range(40 if version == 1 else 60):
            noise = (index % 5 - 2) * 0.2
            shift = 3.0 if index >= 40 else 0.0
            writer.writerow([index, f"{2 * index + 5 + noise + shift:.1f}"])


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--version", type=int, choices=(1, 2), default=1)
    parser.add_argument("--output", type=Path, default=ROOT / "data/raw/samples.csv")
    args = parser.parse_args()
    make_data(args.output, args.version)
    print(f"Wrote dataset v{args.version} to {args.output}")


if __name__ == "__main__":
    main()
