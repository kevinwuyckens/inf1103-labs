from Supplier import Supplier
from Product import Product
from PhysicalProduct import PhysicalProduct
from DigitalProduct import DigitalProduct


def main() -> None:
    gadget_supplier = Supplier("S001", "Gadget Hub Supplies", "sales@gadgethub.example.com")
    licence_supplier = Supplier("S002", "Digital Licence Co", "orders@digitallicence.example.com")
    products: list[Product] = [
        PhysicalProduct("P001", "Laptop", 1200.00, 15, gadget_supplier, 2.1),
        DigitalProduct("D001", "Windows 11 Pro", 199.00, 100, licence_supplier, 5400.0)
    ]

    print("update_stock() keeps the same meaning in every subclass")

    for product in products:
        product.update_stock(product.get_stock() - 5)
        print(f"{product.get_name()}: stock {product.get_stock()}, history {product.get_transaction_history()}")

    for product in products:
        try:
            product.update_stock(-1)
        except ValueError as error:
            print(f"{product.get_name()}: update_stock(-1) raised ValueError: {error}")


if __name__ == "__main__":
    main()
