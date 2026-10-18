import unittest
import pandas as pd
from hypothesis_tests import analyze

class AnalysisTests(unittest.TestCase):
    def frame(self):
        return pd.DataFrame({"total_vol": [10, 12, 14, 10, 12, 14],
                             "precipitation (mm)": [1, 1, 1, 0, 0, 0]})
    def test_identical_group_means_are_not_rejected(self):
        result = analyze(self.frame())
        self.assertEqual((result["rows"], result["rainy_hours"], result["dry_hours"]), (6, 3, 3))
        self.assertAlmostEqual(result["welch_t_test"]["p_value"], 1.0)
        self.assertFalse(result["one_way_anova"]["reject_equal_means"])
    def test_missing_columns_fail_clearly(self):
        with self.assertRaisesRegex(ValueError, "Missing required"):
            analyze(pd.DataFrame({"other": [1, 2]}))
    def test_only_one_weather_group_is_rejected(self):
        frame = self.frame(); frame["precipitation (mm)"] = 0
        with self.assertRaisesRegex(ValueError, "Each rain/dry"):
            analyze(frame)
    def test_invalid_values_are_rejected(self):
        for value in (-1, float("nan"), "invalid"):
            with self.subTest(value=value):
                frame = self.frame().astype(object); frame.loc[0, "total_vol"] = value
                with self.assertRaisesRegex(ValueError, "finite, nonnegative"):
                    analyze(frame)
    def test_alpha_must_be_a_probability(self):
        for alpha in (0, 1, -0.1):
            with self.assertRaisesRegex(ValueError, "alpha"):
                analyze(self.frame(), alpha)

if __name__ == "__main__":
    unittest.main()
