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