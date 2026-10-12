"""Check the example's data contract and deterministic artifacts."""

import csv
import tempfile
import unittest
from pathlib import Path

from scripts.make_data import make_data
from scripts.train import fit_and_evaluate, write_json


class ExampleTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.data = Path(self.directory.name) / "samples.csv"

    def test_dataset_versions_are_repeatable_and_append_rows(self):
        make_data(self.data, 1)
        first = self.data.read_bytes()
        make_data(self.data, 1)
        self.assertEqual(self.data.read_bytes(), first)
        make_data(self.data, 2)
        self.assertTrue(self.data.read_bytes().startswith(first))
        with self.data.open(newline="", encoding="utf-8") as stream:
            self.assertEqual(len(list(csv.DictReader(stream))), 60)

    def test_perfect_line_is_fitted_and_evaluated_on_holdout(self):
        self.data.write_text("x,y\n0,5\n1,7\n2,9\n3,11\n4,13\n", encoding="utf-8")
        model, metrics = fit_and_evaluate(self.data, 0.8)
        self.assertEqual(model["slope"], 2)
        self.assertEqual(model["intercept"], 5)
        self.assertEqual(metrics, {"test_mse": 0, "train_rows": 4, "test_rows": 1})

    def test_new_data_changes_model_and_metrics(self):
        make_data(self.data, 1)
        first = fit_and_evaluate(self.data, 0.8)
        make_data(self.data, 2)
        second = fit_and_evaluate(self.data, 0.8)
        self.assertNotEqual(first[0], second[0])
        self.assertGreater(second[1]["test_mse"], first[1]["test_mse"])

    def test_invalid_splits_are_rejected(self):
        make_data(self.data, 1)
        for fraction in (0, 1, -0.1, 0.01, float("nan"), float("inf")):
            with self.subTest(fraction=fraction), self.assertRaises(ValueError):
                fit_and_evaluate(self.data, fraction)

    def test_invalid_datasets_are_rejected(self):
        for contents in ("x,z\n0,1\n", "x,y\n", "x,y\n1,2\n1,3\n1,4\n", "x,y\n0,nan\n1,2\n2,3\n"):
            with self.subTest(contents=contents):
                self.data.write_text(contents, encoding="utf-8")
                with self.assertRaises(ValueError):
                    fit_and_evaluate(self.data, 0.8)

    def test_json_artifacts_have_stable_bytes(self):
        output = Path(self.directory.name) / "models/model.json"
        write_json(output, {"slope": 2, "intercept": 5})
        first = output.read_bytes()
        write_json(output, {"intercept": 5, "slope": 2})
        self.assertEqual(output.read_bytes(), first)
        self.assertNotIn(b"\r", first)


if __name__ == "__main__":
    unittest.main()
