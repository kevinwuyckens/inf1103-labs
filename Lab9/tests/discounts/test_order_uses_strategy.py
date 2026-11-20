import unittest
from Supplier import Supplier
from ProductFactory import ProductFactory
from Order import Order
from DiscountStrategy import DiscountStrategy
from NoDiscount import NoDiscount
from PercentageDiscount import PercentageDiscount
from BulkDiscount import BulkDiscount


class HalfPriceDiscount(DiscountStrategy):

    def apply(self, total: float) -> float:
        return total / 2


def make_order(discount: DiscountStrategy | None = None) -> Order:
    supplier = Supplier("S001", "Gadget Hub Supplies", "sales@gadgethub.example.com")
    desk_lamp = ProductFactory.create("physical", "P001", "Desk Lamp", 25.00, 10, supplier)
    order = Order("O001", discount)
    order.add_order_line(desk_lamp, 10)
    return order


class TestOrderUsesStrategy(unittest.TestCase):

    def test_order_defaults_to_no_discount(self) -> None:
        order = make_order()
        self.assertIsInstance(order.get_discount(), NoDiscount)
        self.assertEqual(order.calculate_total(), 250.0)

    def test_order_uses_given_strategy(self) -> None:
        order = make_order(BulkDiscount(200, 20))
        self.assertEqual(order.calculate_total(), 230.0)

    def test_set_discount_changes_strategy_on_existing_order(self) -> None:
        order = make_order(BulkDiscount(200, 20))
        order.set_discount(PercentageDiscount(10))
        self.assertEqual(order.calculate_total(), 225.0)

    def test_new_strategy_works_without_changing_order(self) -> None:
        order = make_order(HalfPriceDiscount())
        self.assertEqual(order.calculate_total(), 125.0)


if __name__ == "__main__":
    unittest.main()
