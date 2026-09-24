def get_valid_input():
    '''Prompts until the user enters a non-negative integer or "quit", and returns it with the number of failed attempts'''
    # initialise failed_entries to 0
    failed_entries = 0

    while True:
        # ask for input
        new_value = input("Please enter your stock quantity to add to the inventory: ").lower().strip()

        # if input is quit then return response of "quit"
        if new_value =="quit":
            return new_value, failed_entries

        # if input is valid positive integer then convert response to int for future calculations and return
        elif new_value.isdigit():
            new_value = int(new_value)
            return new_value, failed_entries
        
        # invalid inputs
        # while loop doesn't break so will keep asking user for input until either of the 2 previous conditions are met
        else:
            # negative integers
            if new_value.startswith("-") and new_value[1:].isdigit():
                print("Invalid input. Negative stock quantity not allowed.")
            # everything else
            else:
                print("Invalid input. Please enter a valid, non-negative integer.")

            # increment failed entries for tracking
            failed_entries += 1

def process_delivery(current_total, new_value, max_inventory):
    '''Adds new_value to current_total, capping the total at max_inventory, 
    and returns the new total and any units that could not be added'''
    current_total += new_value
  
    # handles max inventory overflow
    # if current is more than max, add new_value until inventory is full
    # calculates deliveries left over that wasnt successfully added to inventory, units_unprocessed 
    units_unprocessed = 0
    if current_total > max_inventory:
        units_unprocessed = current_total - max_inventory
        current_total = max_inventory

    return current_total, units_unprocessed

def calculate_tax(amount, tax_rate=0.1):
    '''Returns the tax on a delivery amount at the given tax rate'''
    return amount * tax_rate

def generate_report(total_units, total_failed_entries, units_unprocessed):
    '''Prints the final inventory summary'''
    print(f"Total units in inventory: {total_units}")
    print(f"Failed entries: {total_failed_entries}")
    print(f"Units unprocessed: {units_unprocessed}")

def main():
    '''Runs the inventory auditor loop until the user quits or the inventory limit is exceeded'''
    current_total = 0
    total_failed_entries = 0
    units_unprocessed = 0
    max_inventory = 500

    while True:
        new_value, failed_entries = get_valid_input()   
        total_failed_entries += failed_entries

        if new_value == "quit":
            break

        current_total, units_unprocessed = process_delivery(current_total, new_value, max_inventory)

        if units_unprocessed > 0:
            total_failed_entries += 1
            print(f"ALERT: Maximum {max_inventory} units in inventory exceeded. Stopping...")
            break

        tax = calculate_tax(new_value)                              
        print(f"Delivery added: {new_value} units | Tax: {tax} | Running total: {current_total}")

    generate_report(current_total, total_failed_entries, units_unprocessed)

main()