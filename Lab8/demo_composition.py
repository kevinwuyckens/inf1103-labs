from Supplier import Supplier
from PhysicalProduct import PhysicalProduct
from DigitalProduct import DigitalProduct
from Order import Order


def main() -> None:
    supplier = Supplier("S001", "Gadget Hub Supplies", "sales@gadgethub.example.com")
    laptop = PhysicalProduct("P001", "Laptop", 1200.00, 15, supplier, 2.1)
    mouse = PhysicalProduct("P002", "Wireless Mouse", 25.50, 40, supplier, 0.1)
    ebook = DigitalProduct("D001", "Python E-Book", 30.00, 50, supplier, 15.5)

    order_1 = Order("O001")
    order_1.add_order_line(laptop, 1)
    order_1.add_order_line(mouse, 2)
    order_1.add_order_line(ebook, 1)

    order_2 = Order("O002")
    order_2.add_order_line(laptop, 1)

    print("Composition: Order and OrderLine")
    order_1.display_information()
    order_2.display_information()

    line_1 = order_1.get_order_lines()[0]
    line_2 = order_2.get_order_lines()[0]
    print(f"\nThe two laptop lines are the same OrderLine object: {line_1 is line_2}")
    print(f"The two laptop lines refer to the same Product object: {line_1.get_product() is line_2.get_product()}")

    del order_2

    print("\nAfter del order_2, the laptop still exists:")
    laptop.display_information()


if __name__ == "__main__":
    main()
