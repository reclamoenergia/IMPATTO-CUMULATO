import unittest

from calculator import ImpactComponent, InvalidImpactData, compute_cumulative_impact


class CalculatorTests(unittest.TestCase):
    def test_weighted_average(self):
        result = compute_cumulative_impact(
            [
                ImpactComponent("a", 1.0, 1.0),
                ImpactComponent("b", 0.0, 1.0),
                ImpactComponent("c", 0.5, 2.0),
            ]
        )
        self.assertAlmostEqual(result, 0.5)

    def test_rejects_invalid_value_range(self):
        with self.assertRaises(InvalidImpactData):
            compute_cumulative_impact([ImpactComponent("bad", 1.5, 1.0)])

    def test_rejects_negative_weight(self):
        with self.assertRaises(InvalidImpactData):
            compute_cumulative_impact([ImpactComponent("bad", 0.7, -0.1)])


if __name__ == "__main__":
    unittest.main()
