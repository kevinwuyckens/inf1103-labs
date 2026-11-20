import io
import os
import unittest
from contextlib import redirect_stdout
from Inventory import Inventory
from Supplier import Supplier
from inventory_manager import load_products

PRODUCTS_CSV = os.path.join(os.path.dirname(__file__), "..", "..", "products.csv")


class TestLoadProducts(unittest.TestCase):

    def setUp(self) -> None:
        self.inventory = Inventory()
        self.supplier = Supplier("S001", "Gadget Hub Supplies", "sales@gadgethub.example.com")

    def load(self, path: str) -> str:
        output = io.StringIO()
        with redirect_stdout(output):
            load_products(path, self.inventory, self.supplier)
        return output.getvalue()

    def test_valid_rows_load_and_bad_rows_are_skipped(self) -> None:
        output = self.load(PRODUCTS_CSV)
        product_ids = [product.get_product_id() for product in self.inventory.get_products()]

        self.assertEqual(product_ids, ["P001", "D001", "P003"])
        self.assertIn("Skipped row 4: Unknown product type: service", output)
        self.assertIn("Skipped row 5:", output)
        self.assertIn("3 products loaded.", output)
        self.assertIn("Load attempt finished.", output)

    def test_missing_file_is_handled(self) -> None:
        output = self.load("missing.csv")

        self.assertEqual(self.inventory.get_products(), [])
        self.assertIn("Products file not found: missing.csv", output)
        self.assertNotIn("products loaded", output)
        self.assertIn("Load attempt finished.", output)


if __name__ == "__main__":
    unittest.main()
