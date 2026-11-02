import json
import os

INVENTORY_FILE = "inventory.json"

TITLE_LINE = "=" * 40
MENU_LINE = "-" * 28
DIVIDER_LINE = "-" * 45


class Product:
    '''Represents and manages a single product in the inventory'''

    def __init__(self, product_id, name, price, stock, transaction_history=None):
        '''Creates a product, the starting stock becomes the first transaction if no history is given'''
        # double underscore marks each attribute as private
        # code outside the class should use the public methods below instead of changing these directly
        self.__product_id = product_id
        self.__name = name
        self.__price = price
        self.__stock = stock

        # a product loaded from inventory.json already has a history, a brand new product starts with its opening stock
        if transaction_history is None:
            self.__transaction_history = [stock]
        else:
            self.__transaction_history = list(transaction_history)

    def get_product_id(self):
        '''Returns the product id'''
        return self.__product_id

    def get_name(self):
        '''Returns the product name'''
        return self.__name

    def get_price(self):
        '''Returns the product price'''
        return self.__price

    def get_stock(self):
        '''Returns the current stock quantity'''
        return self.__stock

    def get_transaction_history(self):
        '''Returns a copy of the transaction history'''
        # return a copy so code outside the class cannot change the history without going through update_stock
        return list(self.__transaction_history)

    def update_stock(self, quantity):
        '''Replaces the stock with a new quantity and records the change in the transaction history'''
        # the product controls its own stock, so it refuses a value that would put it in an invalid state
        if quantity < 0:
            raise ValueError("Stock quantity cannot be negative.")

        # record how much the stock changed (positive for a delivery, negative for a sale)
        # so the full history of transactions is kept, not just the running total
        change = quantity - self.__stock
        if change != 0:
            self.__transaction_history.append(change)

        self.__stock = quantity


def load_inventory():
    '''Reads every product and its transaction history from inventory.json and returns a list of Product objects'''
    # check whether inventory.json exists before trying to open it
    # if the file does not exist, start with an empty inventory instead of crashing
    if not os.path.exists(INVENTORY_FILE):
        print(f"\n{INVENTORY_FILE} not found. Starting with an empty inventory.")
        return []

    print(f"\n{INVENTORY_FILE} found.")

    # open file in read mode and convert the JSON text back into a list of dictionaries
    # if the file has been damaged and is not valid JSON, start with an empty inventory instead of crashing
    try:
        with open(INVENTORY_FILE, "r") as file:
            data = json.load(file)
    except json.JSONDecodeError:
        print(f"{INVENTORY_FILE} could not be read. Starting with an empty inventory.")
        return []

    # turn each dictionary from the file into a Product object
    inventory = []
    for item in data:
        product = Product(item["id"], item["name"], item["price"], item["stock"], item["transaction_history"])
        inventory.append(product)

    print("Inventory loaded successfully.")
    return inventory


def save_inventory(inventory):
    '''Writes every product and its transaction history to inventory.json'''
    # JSON cannot store Product objects directly, so turn each one back into a dictionary using its public methods
    data = []
    for product in inventory:
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


def display_menu():
    '''Prints the list of menu options'''
    print("\n----------- MENU -----------")
    print("1. Display All Products")
    print("2. Add Product")
    print("3. Update Stock")
    print("4. Search Product")
    print("5. Save Inventory")
    print("6. Exit")
    print(MENU_LINE)


def find_product(inventory, product_id):
    '''Returns the product with the matching product_id, or None if it is not in the inventory'''
    # find the product in inventory given the product_id
    # if cannot find then return None
    for product in inventory:
        if product.get_product_id() == product_id:
            return product
    return None


def get_valid_price():
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


def get_valid_stock(prompt):
    '''Prompts until the user enters a stock quantity of 0 or more, and returns it'''
    while True:
        user_input = input(prompt).strip()

        # isdecimal() is False for negatives, decimals and text, so only whole numbers 0 or more are accepted
        if user_input.isdecimal():
            return int(user_input)

        print("Invalid input. Please enter a whole number of 0 or more.")


def display_all(inventory):
    '''Prints the id, name, price and stock of every product in the inventory'''
    print("\nCurrent Inventory")
    print(DIVIDER_LINE)

    if len(inventory) == 0:
        print("No products in inventory.")

    for product in inventory:
        print(f"ID: {product.get_product_id()} | Name: {product.get_name()} | Price: ${product.get_price():.2f} | Stock: {product.get_stock()}")

    print(DIVIDER_LINE)


def add_product(inventory):
    '''Asks for the details of a new product and adds it to the inventory'''
    print("\nAdd New Product")

    # product ids are stored in uppercase so "p004" and "P004" are treated as the same product
    product_id = input("Product ID: ").strip().upper()

    # product id cannot be empty or already used, otherwise search and update would not know which product to use
    if product_id == "":
        print("\nInvalid input. Product ID cannot be empty.")
        return
    if find_product(inventory, product_id) is not None:
        print(f"\nProduct {product_id} already exists. Use Update Stock to change its stock.")
        return

    # keep asking until a name is entered
    name = input("Product Name: ").strip()
    while name == "":
        print("Invalid input. Product name cannot be empty.")
        name = input("Product Name: ").strip()

    price = get_valid_price()
    stock = get_valid_stock("Stock Quantity: ")

    # each product is a Product object
    # the constructor records the starting stock as the first transaction in its history
    product = Product(product_id, name, price, stock)

    # inventory is a list so it is updated directly, no need to return anything
    inventory.append(product)
    print("\nProduct added successfully!")


def update_stock(inventory):
    '''Finds a product by id and asks the product to update its stock'''
    print("\nUpdate Stock")
    product_id = input("Enter Product ID: ").strip().upper()
    product = find_product(inventory, product_id)

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


def search_product(inventory):
    '''Finds a product by id and prints all of its details'''
    print("\nSearch Product")
    product_id = input("Enter Product ID: ").strip().upper()
    product = find_product(inventory, product_id)

    # product id does not exist in the inventory
    if product is None:
        print("\nProduct not found.")
        return

    print("\nProduct Found")
    print(DIVIDER_LINE)
    print(f"ID: {product.get_product_id()}")
    print(f"Name: {product.get_name()}")
    print(f"Price: ${product.get_price():.2f}")
    print(f"Stock: {product.get_stock()}")
    print(DIVIDER_LINE)


def main():
    '''Shows the menu and runs the chosen option until the user exits'''
    print(TITLE_LINE)
    print("INVENTORY MANAGEMENT SYSTEM")
    print(TITLE_LINE)

    # loads inventory from inventory.json, or an empty list if the file does not exist
    inventory = load_inventory()

    display_menu()
    exit_program = False

    while not exit_program:
        option = input("\nEnter option: ").strip()

        if option == "1":
            display_all(inventory)
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
