from DigitalProduct import DigitalProduct
from PhysicalProduct import PhysicalProduct
from Product import Product
from Supplier import Supplier


class ProductFactory:

    @staticmethod
    def create(product_type: str, product_id: str, name: str, price: float, stock_quantity: int, supplier: Supplier,
               weight: float = 0.0, download_size: float = 0.0, transaction_history: list[int] | None = None) -> Product:
        if product_type == "physical":
            return PhysicalProduct(product_id, name, price, stock_quantity, supplier, weight, transaction_history)
        elif product_type == "digital":
            return DigitalProduct(product_id, name, price, stock_quantity, supplier, download_size, transaction_history)
        else:
            raise ValueError(f"Unknown product type: {product_type}")
