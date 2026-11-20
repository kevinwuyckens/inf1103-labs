import unittest
from NoDiscount import NoDiscount
from PercentageDiscount import PercentageDiscount
from BulkDiscount import BulkDiscount
from StudentDiscount import StudentDiscount


class TestDiscountStrategies(unittest.TestCase):

    def test_no_discount_returns_total_unchanged(self) -> None:
        self.assertEqual(NoDiscount().apply(250.0), 250.0)

    def test_percentage_discount(self) -> None:
        self.assertEqual(PercentageDiscount(10).apply(250.0), 225.0)

    def test_bulk_discount_at_or_above_threshold(self) -> None:
        self.assertEqual(BulkDiscount(200, 20).apply(250.0), 230.0)
        self.assertEqual(BulkDiscount(200, 20).apply(200.0), 180.0)

    def test_bulk_discount_below_threshold(self) -> None:
        self.assertEqual(BulkDiscount(200, 20).apply(199.0), 199.0)

    def test_student_discount(self) -> None:
        self.assertEqual(StudentDiscount().apply(250.0), 237.5)


if __name__ == "__main__":
    unittest.main()
