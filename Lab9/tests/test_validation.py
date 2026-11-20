import unittest
from Supplier import Supplier
from ProductFactory import ProductFactory
from OrderLine import OrderLine
from PercentageDiscount import PercentageDiscount
from BulkDiscount import BulkDiscount


class TestValidation(unittest.TestCase):

    def setUp(self) -> None:
        self.supplier = Supplier("S001", "Gadget Hub Supplies", "sales@gadgethub.example.com")
        self.product = ProductFactory.create("physical", "P001", "Desk Lamp", 25.00, 10, self.supplier)

    def test_price_must_be_greater_than_zero(self) -> None:
        for price in [0, -5]:
            with self.subTest(price=price):
                with self.assertRaises(ValueError):
                    ProductFactory.create("physical", "P002", "Office Chair", price, 3, self.supplier)

    def test_stock_cannot_be_negative(self) -> None:
        for product_type in ["physical", "digital"]:
            with self.subTest(product_type=product_type):
                with self.assertRaises(ValueError):
                    ProductFactory.create(product_type, "P003", "Monitor Stand", 39.50, -1, self.supplier)

    def test_update_stock_cannot_be_negative(self) -> None:
        with self.assertRaises(ValueError):
            self.product.update_stock(-1)
        self.assertEqual(self.product.get_stock(), 10)

    def test_order_quantity_must_be_greater_than_zero(self) -> None:
        for quantity in [0, -2]:
            with self.subTest(quantity=quantity):
                with self.assertRaises(ValueError):
                    OrderLine(self.product, quantity)

    def test_valid_values_are_accepted(self) -> None:
        product = ProductFactory.create("digital", "D001", "Photo Editor", 49.90, 0, self.supplier)
        order_line = OrderLine(product, 1)
        self.assertEqual(product.get_stock(), 0)
        self.assertEqual(order_line.get_quantity(), 1)

    def test_invalid_discount_settings_are_rejected(self) -> None:
        with self.assertRaises(ValueError):
            PercentageDiscount(150)
        with self.assertRaises(ValueError):
            BulkDiscount(200, 300)


if __name__ == "__main__":
    unittest.main()
