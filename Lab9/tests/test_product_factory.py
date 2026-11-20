import unittest
from Supplier import Supplier
from Product import Product
from PhysicalProduct import PhysicalProduct
from DigitalProduct import DigitalProduct
from ProductFactory import ProductFactory


class TestProductFactory(unittest.TestCase):

    def setUp(self) -> None:
        self.supplier = Supplier("S001", "Gadget Hub Supplies", "sales@gadgethub.example.com")

    def test_creates_physical_product(self) -> None:
        product = ProductFactory.create("physical", "P001", "Desk Lamp", 25.00, 10, self.supplier, weight=0.5)
        self.assertIsInstance(product, PhysicalProduct)
        self.assertIsInstance(product, Product)
        self.assertEqual(product.get_name(), "Desk Lamp")

    def test_creates_digital_product(self) -> None:
        product = ProductFactory.create("digital", "D001", "Photo Editor", 49.90, 100, self.supplier, download_size=300)
        self.assertIsInstance(product, DigitalProduct)
        self.assertIsInstance(product, Product)
        self.assertEqual(product.get_name(), "Photo Editor")

    def test_unknown_type_raises_value_error(self) -> None:
        with self.assertRaises(ValueError) as context:
            ProductFactory.create("service", "S001", "Installation", 30.00, 5, self.supplier)
        self.assertEqual(str(context.exception), "Unknown product type: service")


if __name__ == "__main__":
    unittest.main()
