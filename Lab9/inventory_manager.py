import json
from Supplier import Supplier
from Product import Product
from ProductFactory import ProductFactory
from CanBeShipped import CanBeShipped
from Inventory import Inventory
from Order import Order
from DiscountStrategy import DiscountStrategy
from NoDiscount import NoDiscount
from PercentageDiscount import PercentageDiscount
from BulkDiscount import BulkDiscount
from StudentDiscount import StudentDiscount

INVENTORY_FILE = "inventory.json"
TITLE_LINE = "=" * 40
MENU_LINE = "-" * 25
DIVIDER_LINE = "-" * 40


def find_supplier(suppliers: list[Supplier], supplier_id: str) -> Supplier | None:
    for supplier in suppliers:
        if supplier.get_supplier_id() == supplier_id:
            return supplier
    return None


def load_data() -> tuple[list[Supplier], Inventory]:
    suppliers: list[Supplier] = []
    inventory = Inventory()

    try:
        with open(INVENTORY_FILE, "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        print(f"\n{INVENTORY_FILE} not found. Starting with an empty inventory.")
        return suppliers, inventory
    except json.JSONDecodeError:
        print(f"\n{INVENTORY_FILE} is not valid JSON. Starting with an empty inventory.")
        return suppliers, inventory

    for item in data["suppliers"]:
        suppliers.append(Supplier(item["id"], item["name"], item["contact_email"]))

    for item in data["products"]:
        supplier = find_supplier(suppliers, item["supplier_id"])
        if supplier is None:
            print(f"Unknown supplier '{item['supplier_id']}' for product {item['id']}, skipped.")
            continue

        try:
            product = ProductFactory.create(item["type"], item["id"], item["name"], item["price"], item["stock"], supplier,
                                            weight=item.get("weight", 0.0),
                                            download_size=item.get("download_size", 0.0),
                                            transaction_history=item["transaction_history"])
        except ValueError as error:
            print(f"Product {item['id']} skipped: {error}")
            continue

        inventory.add_product(product)

    print(f"\n{INVENTORY_FILE} loaded successfully.")
    return suppliers, inventory


def save_data(suppliers: list[Supplier], inventory: Inventory) -> None:
    supplier_data: list[dict[str, str]] = []
    for supplier in suppliers:
        supplier_data.append(supplier.to_dictionary())

    product_data: list[dict[str, str | int | float | list[int]]] = []
    for product in inventory.get_products():
        product_data.append(product.to_dictionary())

    with open(INVENTORY_FILE, "w") as file:
        json.dump({"suppliers": supplier_data, "products": product_data}, file)


def display_menu() -> None:
    print("\n----------- MENU -----------")
    print("1. Display All Products")
    print("2. Add Product")
    print("3. Update Stock")
    print("4. Search Product")
    print("5. Remove Product")
    print("6. Display Suppliers")
    print("7. Add Supplier")
    print("8. Create Order")
    print("9. Save Inventory")
    print("10. Exit")
    print(MENU_LINE)


def get_positive_float(prompt: str) -> float:
    while True:
        try:
            value = float(input(prompt))
            if value <= 0:
                print("Please enter a number greater than zero.")
                continue
            return value
        except ValueError:
            print("Please enter a valid number, e.g. 12.50")


def get_valid_product_type() -> str:
    print("Product Type:")
    print("1. Physical")
    print("2. Digital")

    while True:
        choice = input("Choose product type (1 or 2): ").strip()

        if choice == "1":
            return "physical"
        if choice == "2":
            return "digital"

        print("Invalid input. Please enter 1 or 2.")


def get_valid_stock(prompt: str) -> int:
    while True:
        try:
            value = int(input(prompt))

            if value < 0:
                print("Stock quantity cannot be negative.")
                continue
            return value
        except ValueError:
            print("Please enter a whole number, e.g. 10")


def get_valid_quantity(prompt: str) -> int:
    while True:
        try:
            value = int(input(prompt))
            if value <= 0:
                print("Please enter a quantity greater than zero.")
                continue
            return value
        except ValueError:
            print("Please enter a whole number, e.g. 2")


def display_suppliers(suppliers: list[Supplier]) -> None:
    print("\nSuppliers")
    print(DIVIDER_LINE)

    if len(suppliers) == 0:
        print("No suppliers found.")

    for supplier in suppliers:
        supplier.display_information()

    print(DIVIDER_LINE)


def get_valid_supplier(suppliers: list[Supplier]) -> Supplier:
    display_suppliers(suppliers)

    while True:
        supplier_id = input("Supplier ID: ").strip().upper()
        supplier = find_supplier(suppliers, supplier_id)

        if supplier is not None:
            return supplier

        print("Invalid input. Please enter one of the supplier IDs above.")


def add_product(inventory: Inventory, suppliers: list[Supplier]) -> None:
    print("\nAdd New Product")

    product_id = input("Product ID: ").strip().upper()

    if product_id == "":
        print("\nInvalid input. Product ID cannot be empty.")
        return
    if inventory.find_product(product_id) is not None:
        print(f"\nProduct {product_id} already exists. Use Update Stock to change its stock.")
        return

    if len(suppliers) == 0:
        print("\nNo suppliers found. Every product needs a supplier, so add a supplier first.")
        return

    product_type = get_valid_product_type()

    name = input("Product Name: ").strip()
    while name == "":
        print("Invalid input. Product name cannot be empty.")
        name = input("Product Name: ").strip()

    price = get_positive_float("Price: ")
    stock = get_valid_stock("Stock Quantity: ")

    supplier = get_valid_supplier(suppliers)

    weight = 0.0
    download_size = 0.0
    if product_type == "physical":
        weight = get_positive_float("Weight (kg): ")
    else:
        download_size = get_positive_float("Download Size (MB): ")
    try:
        product = ProductFactory.create(product_type, product_id, name, price, stock, supplier,
                                        weight=weight, download_size=download_size)
    except ValueError as error:
        print(f"\nProduct not added: {error}")
        return

    inventory.add_product(product)
    print("\nProduct added successfully!")


def update_stock(inventory: Inventory) -> None:
    print("\nUpdate Stock")
    product_id = input("Enter Product ID: ").strip().upper()
    product = inventory.find_product(product_id)

    if product is None:
        print("\nProduct not found.")
        return

    print("\nProduct Found:")
    print(f"Name: {product.get_name()}")
    print(f"Current Stock: {product.get_stock()}")
    print()

    new_stock = get_valid_stock("New Stock Quantity: ")

    product.update_stock(new_stock)
    print("\nStock updated successfully!")


def show_product_details(product: Product) -> None:
    product.display_details()
    print(f"Fulfilment: {product.get_fulfilment_info()}")


def search_product(inventory: Inventory) -> None:
    print("\nSearch Product")
    product_id = input("Enter Product ID: ").strip().upper()
    product = inventory.find_product(product_id)

    if product is None:
        print("\nProduct not found.")
        return

    print("\nProduct Found")
    print(DIVIDER_LINE)
    show_product_details(product)

    if isinstance(product, CanBeShipped):
        print(f"Shipping Cost: ${product.calculate_shipping_cost():.2f}")

    print(DIVIDER_LINE)


def remove_product(inventory: Inventory) -> None:
    print("\nRemove Product")
    product_id = input("Enter Product ID: ").strip().upper()

    product = inventory.remove_product(product_id)

    if product is None:
        print("\nProduct not found.")
        return

    print(f"\nProduct {product.get_product_id()} ({product.get_name()}) removed from inventory.")


def add_supplier(suppliers: list[Supplier]) -> None:
    print("\nAdd New Supplier")

    supplier_id = input("Supplier ID: ").strip().upper()

    if supplier_id == "":
        print("\nInvalid input. Supplier ID cannot be empty.")
        return
    if find_supplier(suppliers, supplier_id) is not None:
        print(f"\nSupplier {supplier_id} already exists.")
        return

    name = input("Supplier Name: ").strip()
    while name == "":
        print("Invalid input. Supplier name cannot be empty.")
        name = input("Supplier Name: ").strip()

    contact_email = input("Contact Email: ").strip()
    while "@" not in contact_email:
        print("Invalid input. Please enter a valid email address.")
        contact_email = input("Contact Email: ").strip()

    suppliers.append(Supplier(supplier_id, name, contact_email))
    print("\nSupplier added successfully!")


def choose_discount() -> DiscountStrategy:
    print("\nDiscount Options")
    print("1. No Discount")
    print("2. Percentage Discount")
    print("3. Bulk Discount")
    print("4. Student Discount (5%)")

    while True:
        choice = input("Choose discount (1-4): ").strip()

        try:
            if choice == "1":
                return NoDiscount()
            if choice == "2":
                percentage = get_positive_float("Percentage off: ")
                return PercentageDiscount(percentage)
            if choice == "3":
                threshold = get_positive_float("Minimum order total: ")
                amount = get_positive_float("Amount off: ")
                return BulkDiscount(threshold, amount)
            if choice == "4":
                return StudentDiscount()
            
        except ValueError as error:
            print(f"Invalid discount: {error}")
            continue
        print("Invalid input. Please enter a number from 1 to 4.")


def create_order(inventory: Inventory) -> None:
    print("\nCreate Order")

    order_id = input("Order ID: ").strip().upper()
    if order_id == "":
        print("\nInvalid input. Order ID cannot be empty.")
        return

    order = Order(order_id)

    while True:
        product_id = input("\nProduct ID (press Enter to finish): ").strip().upper()
        if product_id == "":
            break

        product = inventory.find_product(product_id)
        if product is None:
            print("Product not found.")
            continue

        quantity = get_valid_quantity("Quantity: ")

        order.add_order_line(product, quantity)
        print(f"Added {quantity} x {product.get_name()} to order {order_id}.")

    if len(order.get_order_lines()) == 0:
        order.display_information()
        return

    order.set_discount(choose_discount())
    order.display_information()

    while input("\nChange discount? (y/n): ").strip().lower() == "y":
        order.set_discount(choose_discount())
        order.display_information()


def main() -> None:
    print(TITLE_LINE)
    print("INVENTORY MANAGEMENT SYSTEM")
    print(TITLE_LINE)

    suppliers, inventory = load_data()

    display_menu()
    exit_program = False

    while not exit_program:
        option = input("\nEnter option: ").strip()

        if option == "1":
            inventory.display_all()
        elif option == "2":
            add_product(inventory, suppliers)
        elif option == "3":
            update_stock(inventory)
        elif option == "4":
            search_product(inventory)
        elif option == "5":
            remove_product(inventory)
        elif option == "6":
            display_suppliers(suppliers)
        elif option == "7":
            add_supplier(suppliers)
        elif option == "8":
            create_order(inventory)
        elif option == "9":
            print("\nSaving inventory...")
            save_data(suppliers, inventory)
            print(f"Inventory saved successfully to {INVENTORY_FILE}.")
        elif option == "10":
            print("\nSaving inventory before exit...")
            save_data(suppliers, inventory)
            print("Inventory saved successfully.")
            print("\nThank you for using Inventory Management System.")
            print("Program terminated.")
            exit_program = True
        else:
            print("Invalid option. Please enter a number from 1 to 10.")
            display_menu()

if __name__ == "__main__":
    main()
