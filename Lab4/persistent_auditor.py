EXIT_SIGNAL = -99
MAX_CAPACITY = 500
TAX_RATE = 0.1
INVENTORY_FILE = "inventory.txt"
FIELD_SEPARATOR = ","
HISTORY_SEPARATOR = "|"

ITEM_FIELDS = {
    "id": 0,
    "name": 1,
    "quantity": 2,
    "transaction_history": 3
}


def load_inventory():
    '''Reads every item and its transaction history from inventory.txt and returns the inventory'''
    inventory = []

    # open file in read mode
    # if the file does not exist, start with an empty inventory instead of crashing
    try:
        with open(INVENTORY_FILE, "r") as file:
            lines = file.readlines()
    except FileNotFoundError:
        print(f"{INVENTORY_FILE} not found. Starting with an empty inventory.")

        return inventory

    # for each line in the inventory file
    for line in lines:
        # remove the newline at the end and skip any blank lines
        line = line.strip()
        if line == "":
            continue

        # split the line into its fields
        fields = line.split(FIELD_SEPARATOR)
        item_id = fields[ITEM_FIELDS["id"]]
        name = fields[ITEM_FIELDS["name"]]
        quantity = int(fields[ITEM_FIELDS["quantity"]])
        history = fields[ITEM_FIELDS["transaction_history"]]

        # split the history into a list of amounts, so "5|10|5" becomes 5, 10, 5
        # if the item has no history yet, leave the list empty
        transaction_history = []
        if history != "":
            for amount in history.split(HISTORY_SEPARATOR):
                transaction_history.append(int(amount))

        # append item and its details to inventory list
        inventory.append([item_id, name, quantity, transaction_history])

    return inventory


def display_inventory(inventory):
    '''Prints the id, name and quantity of every item in the inventory'''
    print("\nCurrent Inventory:")


    if len(inventory) == 0:
        print("No items in inventory.")
    for item in inventory:
        item_id = item[ITEM_FIELDS["id"]]
        name = item[ITEM_FIELDS["name"]]
        quantity = item[ITEM_FIELDS["quantity"]]
        print(f"{item_id}, {name}, {quantity}")


def find_item(inventory, item_id):
    '''Returns the item with the matching item_id, or None if it is not in the inventory'''
   
    for item in inventory:
        if item[ITEM_FIELDS["id"]] == item_id:
            return item
    return None


def get_valid_input(item):
    '''Prompts until the user enters a valid stock quantity for the item or "quit", and returns it with the number of failed attempts'''

    failed_entries = 0
    current_quantity = item[ITEM_FIELDS["quantity"]]

    while True:
        # ask for input
        user_input = input("Enter quantity to add (or 'quit'): ").strip().lower()



        if user_input == "quit":
            return EXIT_SIGNAL, failed_entries
        if not user_input.isdigit() or int(user_input) == 0:
            print("Invalid input. Please enter a positive whole number.")
            failed_entries += 1
        elif current_quantity + int(user_input) > MAX_CAPACITY:
            print(f"Invalid input. Maximum capacity is {MAX_CAPACITY} units per item.")
            failed_entries += 1
        else:
            return int(user_input), failed_entries


def process_delivery(item, new_quantity):
    '''Adds new_quantity to the item's quantity'''
    # item is a list so it is updated directly, no need to return anything
    item[ITEM_FIELDS["quantity"]] += new_quantity


def calculate_tax(amount, tax_rate):
    '''Returns the tax on a delivery amount at the given tax rate'''
    return amount * tax_rate


def display_status(item, valid_quantity, tax_amount):
    '''Prints the delivery that was just added and the item updated quantity'''
    name = item[ITEM_FIELDS["name"]]
    quantity = item[ITEM_FIELDS["quantity"]]

    print(f"\nDelivery added: {valid_quantity} units | Tax: {tax_amount:.2f}")
    print(f"{name} now has {quantity} units")


def generate_report(inventory, failed_entries):
    '''Prints the final inventory summary'''
    # add up the quantity of every item to get the total units
    total_units = 0
    for item in inventory:
        total_units += item[ITEM_FIELDS["quantity"]]

    print("\nFinal Report")
    display_inventory(inventory)
    print(f"Total units in inventory: {total_units}")
    print(f"Failed entries: {failed_entries}")


def main():
    '''Runs the inventory auditor loop until the user quits, then prints the report'''
    # loads inventory from inventory.txt
    inventory = load_inventory()
    total_failed_entries = 0
    exit_program = False

    while not exit_program:
        display_inventory(inventory)
        item_id = input("\nEnter item ID (or 'quit'): ").strip().lower()
        item = find_item(inventory, item_id)
        if item_id == "quit":
            exit_program = True
        # item id does not exist in the inventory, count it as a failed entry
        elif item is None:
            print("Item not found. Please try again.")
            total_failed_entries += 1
        else:
            quantity, failed_entries = get_valid_input(item)
            total_failed_entries += failed_entries

            if quantity == EXIT_SIGNAL:
                exit_program = True
            else:
                process_delivery(item, quantity)
                tax_amount = calculate_tax(quantity, TAX_RATE)
                display_status(item, quantity, tax_amount)

    # after quitting, print the final summary
    generate_report(inventory, total_failed_entries)


if __name__ == "__main__":
    main()