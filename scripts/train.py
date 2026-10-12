"""Fit a tiny linear model and write deterministic JSON artifacts.

Only the Python standard library is needed. The model is a vehicle for
learning version control, rather than a model-development tutorial.
"""

import argparse
import csv
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def fit_and_evaluate(data: Path, train_fraction: float) -> tuple[dict, dict]:
    if not math.isfinite(train_fraction) or not 0 < train_fraction < 1:
        raise ValueError("train_fraction must be finite and strictly between 0 and 1.")
    with data.open(encoding="utf-8", newline="") as stream:
        reader = csv.DictReader(stream)
        if reader.fieldnames != ["x", "y"]:
            raise ValueError("Dataset must have exactly the columns x,y.")
        rows = [(float(row["x"]), float(row["y"])) for row in reader]
    if not all(math.isfinite(value) for row in rows for value in row):
        raise ValueError("Dataset values must be finite.")
    split = int(len(rows) * train_fraction)
    if split < 2 or split >= len(rows):
        raise ValueError("The split must leave at least two training rows and one test row.")
    training, test = rows[:split], rows[split:]
    mean_x = sum(x for x, _ in training) / len(training)
    mean_y = sum(y for _, y in training) / len(training)
    variance = sum((x - mean_x) ** 2 for x, _ in training)
    if variance == 0:
        raise ValueError("Training x values must not all be identical.")
    slope = sum((x - mean_x) * (y - mean_y) for x, y in training) / variance
    intercept = mean_y - slope * mean_x
    mse = sum((slope * x + intercept - y) ** 2 for x, y in test) / len(test)
    model = {"type": "linear_regression", "slope": round(slope, 10), "intercept": round(intercept, 10)}
    metrics = {"test_mse": round(mse, 10), "train_rows": len(training), "test_rows": len(test)}
    return model, metrics


def write_json(path: Path, contents: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    # Explicit LF keeps generated artifact hashes stable on Windows.
    with path.open("w", encoding="utf-8", newline="\n") as stream:
        stream.write(json.dumps(contents, indent=2, sort_keys=True, allow_nan=False) + "\n")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", type=Path, default=ROOT / "data/raw/samples.csv")
    parser.add_argument("--params", type=Path, default=ROOT / "params.json")
    parser.add_argument("--model", type=Path, default=ROOT / "models/model.json")
    parser.add_argument("--metrics", type=Path, default=ROOT / "metrics.json")
    args = parser.parse_args()
    params = json.loads(args.params.read_text(encoding="utf-8"))
    model, metrics = fit_and_evaluate(args.data, float(params["train_fraction"]))
    write_json(args.model, model)
    write_json(args.metrics, metrics)
    print(json.dumps(metrics, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
