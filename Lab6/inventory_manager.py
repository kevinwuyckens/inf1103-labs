import json
from Product import Product
from Inventory import Inventory

INVENTORY_FILE = "inventory.json"
TITLE_LINE = "=" * 40
MENU_LINE = "-" * 25

def load_inventory() -> Inventory:
    '''Reads every product and its transaction history from inventory.json and returns an Inventory object'''
    inventory = Inventory()

    # open file in read mode and convert the JSON text back into a list of dictionaries
    # if the file does not exist, start with an empty inventory instead of crashing
    try:
        with open(INVENTORY_FILE, "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        print(f"\n{INVENTORY_FILE} not found. Starting with an empty inventory.")
        return inventory

    # turn each dictionary from the file into a Product object and store it in the inventory
    for item in data:
        product = Product(item["id"], item["name"], item["price"], item["stock"], item["transaction_history"])
        inventory.add_product(product)

    print(f"\n{INVENTORY_FILE} loaded successfully.")
    return inventory


def save_inventory(inventory: Inventory) -> None:
    '''Writes every product and its transaction history to inventory.json'''
    # JSON cannot store Product objects directly, so turn each one back into a dictionary using its public methods
    data = []
    for product in inventory.get_products():
        data.append({
            "id": product.get_product_id(),
            "name": product.get_name(),
            "price": product.get_price(),
            "stock": product.get_stock(),
            "transaction_history": product.get_transaction_history()
        })

    # open file in write mode, this replaces the old contents of the file
    with open(INVENTORY_FILE, "w") as file:
        json.dump(data, file)


def display_menu() -> None:
    '''Prints the list of menu options'''
    print("\n----------- MENU -----------")
    print("1. Display All Products")
    print("2. Add Product")
    print("3. Update Stock")
    print("4. Search Product")
    print("5. Save Inventory")
    print("6. Exit")
    print(MENU_LINE)


def get_valid_price() -> float:
    '''Prompts until the user enters a price greater than 0, and returns it'''
    while True:
        user_input = input("Price: ").strip()

        # float() raises ValueError if the input is not a number, e.g. "abc"
        try:
            price = float(user_input)
        except ValueError:
            print("Invalid input. Please enter a number.")
            continue

        # a product cannot be free or have a negative price
        if price <= 0:
            print("Invalid input. Price must be greater than 0.")
        else:
            return price


def get_valid_stock(prompt: str) -> int:
    '''Prompts until the user enters a stock quantity of 0 or more, and returns it'''
    while True:
        user_input = input(prompt).strip()

        # isdecimal() is False for negatives, decimals and text, so only whole numbers 0 or more are accepted
        if user_input.isdecimal():
            return int(user_input)

        print("Invalid input. Please enter a whole number of 0 or more.")


def add_product(inventory: Inventory) -> None:
    '''Asks for the details of a new product and adds it to the inventory'''
    print("\nAdd New Product")

    # product ids are stored in uppercase so "p004" and "P004" are treated as the same product
    product_id = input("Product ID: ").strip().upper()

    # check the id before asking for the other details so the user does not type them for nothing
    if product_id == "":
        print("\nInvalid input. Product ID cannot be empty.")
        return
    if inventory.search_product(product_id) is not None:
        print(f"\nProduct {product_id} already exists. Use Update Stock to change its stock.")
        return

    # keep asking until a name is entered
    name = input("Product Name: ").strip()
    while name == "":
        print("Invalid input. Product name cannot be empty.")
        name = input("Product Name: ").strip()

    price = get_valid_price()
    stock = get_valid_stock("Stock Quantity: ")

    # create the Product object and pass it to the inventory to store
    product = Product(product_id, name, price, stock)
    inventory.add_product(product)
    print("\nProduct added successfully!")


def update_stock(inventory: Inventory) -> None:
    '''Finds a product by id and asks the product to update its stock'''
    print("\nUpdate Stock")
    product_id = input("Enter Product ID: ").strip().upper()
    product = inventory.search_product(product_id)

    # product id does not exist in the inventory
    if product is None:
        print("\nProduct not found.")
        return

    print("\nProduct Found:")
    print(f"Name: {product.get_name()}")
    print(f"Current Stock: {product.get_stock()}")
    print()

    new_stock = get_valid_stock("New Stock Quantity: ")

    # the product updates its own stock and transaction history
    product.update_stock(new_stock)
    print("\nStock updated successfully!")


def search_product(inventory: Inventory) -> None:
    '''Finds a product by id and prints all of its details'''
    print("\nSearch Product")
    product_id = input("Enter Product ID: ").strip().upper()
    product = inventory.search_product(product_id)

    # product id does not exist in the inventory
    if product is None:
        print("\nProduct not found.")
        return

    print("\nProduct Found")
    product.display_details()


def main() -> None:
    '''Shows the menu and runs the chosen option until the user exits'''
    print(TITLE_LINE)
    print("INVENTORY MANAGEMENT SYSTEM")
    print(TITLE_LINE)

    # loads inventory from inventory.json, or an empty inventory if the file does not exist
    inventory = load_inventory()

    display_menu()
    exit_program = False

    while not exit_program:
        option = input("\nEnter option: ").strip()

        if option == "1":
            inventory.display_all()
        elif option == "2":
            add_product(inventory)
        elif option == "3":
            update_stock(inventory)
        elif option == "4":
            search_product(inventory)
        elif option == "5":
            print("\nSaving inventory...")
            save_inventory(inventory)
            print(f"Inventory saved successfully to {INVENTORY_FILE}.")
        # user wants to exit, save first so no changes are lost
        elif option == "6":
            print("\nSaving inventory before exit...")
            save_inventory(inventory)
            print("Inventory saved successfully.")
            print("\nThank you for using Inventory Management System.")
            print("Program terminated.")
            exit_program = True
        # anything else is not a menu option, show the menu again so the user can see the choices
        else:
            print("Invalid option. Please enter a number from 1 to 6.")
            display_menu()

if __name__ == "__main__":
    main()
