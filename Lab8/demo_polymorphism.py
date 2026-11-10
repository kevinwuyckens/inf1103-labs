from Supplier import Supplier
from Product import Product
from PhysicalProduct import PhysicalProduct
from DigitalProduct import DigitalProduct
from inventory_manager import show_product_details, DIVIDER_LINE


def main() -> None:
    gadget_supplier = Supplier("S001", "Gadget Hub Supplies", "sales@gadgethub.example.com")
    licence_supplier = Supplier("S002", "Digital Licence Co", "orders@digitallicence.example.com")
    products: list[Product] = [
        PhysicalProduct("P001", "Laptop", 1200.00, 15, gadget_supplier, 2.1),
        DigitalProduct("D001", "Windows 11 Pro", 199.00, 100, licence_supplier, 5400.0)
    ]

    print("Polymorphism: show_product_details(product: Product)")

    for product in products:
        print(DIVIDER_LINE)
        show_product_details(product)



if __name__ == "__main__":
    main()
