TITLE_LINE = "=" * 40
MENU_LINE = "-" * 28
DIVIDER_LINE = "-" * 45


def display_menu():
    '''Prints the list of menu options'''
    print("\n----------- MENU -----------")
    print("1. Display All Products")
    print("2. Add Product")
    print("3. Update Stock")
    print("4. Search Product")
    print("5. Exit")
    print(MENU_LINE)


def find_product(inventory, product_id):
    '''Returns the product with the matching product_id, or None if it is not in the inventory'''
    # find the product in inventory given the product_id
    # if cannot find then return None
    for product in inventory:
        if product["id"] == product_id:
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
        print(f"ID: {product['id']} | Name: {product['name']} | Price: ${product['price']:.2f} | Stock: {product['stock']}")

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

    # each product is a dictionary
    # the starting stock is recorded as the first transaction in its history
    product = {
        "id": product_id,
        "name": name,
        "price": price,
        "stock": stock,
        "transaction_history": [stock]
    }

    # inventory is a list so it is updated directly, no need to return anything
    inventory.append(product)
    print("\nProduct added successfully!")


def update_stock(inventory):
    '''Finds a product by id, replaces its stock with a new quantity and records the change in its transaction history'''
    print("\nUpdate Stock")
    product_id = input("Enter Product ID: ").strip().upper()
    product = find_product(inventory, product_id)

    # product id does not exist in the inventory
    if product is None:
        print("\nProduct not found.")
        return

    print("\nProduct Found:")
    print(f"Name: {product['name']}")
    print(f"Current Stock: {product['stock']}")
    print()

    new_stock = get_valid_stock("New Stock Quantity: ")

    # record how much the stock changed (positive for a delivery, negative for a sale)
    # so the full history of transactions is kept, not just the running total
    change = new_stock - product["stock"]
    if change != 0:
        product["transaction_history"].append(change)

    # product is a dictionary so it is updated directly, no need to return anything
    product["stock"] = new_stock
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
    print(f"ID: {product['id']}")
    print(f"Name: {product['name']}")
    print(f"Price: ${product['price']:.2f}")
    print(f"Stock: {product['stock']}")
    print(DIVIDER_LINE)


def main():
    '''Shows the menu and runs the chosen option until the user exits'''
    print(TITLE_LINE)
    print("INVENTORY MANAGEMENT SYSTEM")
    print(TITLE_LINE)

    # each product is a dictionary and all products are stored in a list
    # the starting stock is recorded as the first transaction in each product's history
    inventory = [
        {"id": "P001", "name": "Laptop", "price": 1200.00, "stock": 15, "transaction_history": [15]},
        {"id": "P002", "name": "Mouse", "price": 25.50, "stock": 40, "transaction_history": [40]},
        {"id": "P003", "name": "Keyboard", "price": 45.00, "stock": 25, "transaction_history": [25]}
    ]

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
        # user wants to exit
        elif option == "5":
            print("\nThank you for using Inventory Management System.")
            print("Program terminated.")
            exit_program = True
        # anything else is not a menu option, show the menu again so the user can see the choices
        else:
            print("Invalid option. Please enter a number from 1 to 5.")
            display_menu()


if __name__ == "__main__":
    main()
