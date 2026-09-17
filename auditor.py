def inventory_function():
    # init variables
    inventory = 0
    failed_entries = 0
    units_unprocessed = 0
    max_inventory = 500

    while True:
            # ask for input
            response = input(f"Current inventory: {inventory}. Please enter your stock quantity to add to the inventory: ").lower().strip()

            # if input is quit then print relevant info, and then break While loop
            if response =="quit":
                break

            # if input is valid non negative integer then add to inventory
            elif response.isdigit():
                inventory += int(response)

                # if inventory doesnt exceed max inventory then increment inventory with the user response
                if inventory <= max_inventory:
                    print(f"You have successfully added {response} to the inventory")

                # if inventory exceeeds max inventory, then set inventory to max and break While loop
                else:
                    units_unprocessed = inventory - max_inventory # calculates leftover units
                    inventory = max_inventory # assume units will be added till inventory is maxed, meaning left over units that are not added
                    failed_entries += 1 # considered failed entry since not all units were added successfully
                    print(f"ALERT: Maximum {max_inventory} units in inventory exceeded. Stopping...")
                break

            # invalid inputs
            else:
                # negative numbers
                if response.startswith("-") and response[1:].isdigit():
                    print("Invalid input. Negative stock quantity not allowed.")
                # everything else
                else:
                    print("Invalid input. Please enter a valid, non-negative integer.")
                failed_entries += 1

inventory_function()