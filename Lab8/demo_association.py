from Supplier import Supplier
from PhysicalProduct import PhysicalProduct
from DigitalProduct import DigitalProduct


def main() -> None:
    supplier = Supplier("S001", "Gadget Hub Supplies", "sales@gadgethub.example.com")
    laptop = PhysicalProduct("P001", "Laptop", 1200.00, 15, supplier, 2.1)
    ebook = DigitalProduct("D001", "Python E-Book", 30.00, 50, supplier, 15.5)

    print("Association: Supplier and Product")
    print(f"Both products refer to the same Supplier object: {laptop.get_supplier() is ebook.get_supplier()}")

    del supplier

    print("\nAfter del supplier:")
    laptop.get_supplier().display_information()
    ebook.get_supplier().display_information()


if __name__ == "__main__":
    main()
