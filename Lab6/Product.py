DIVIDER_LINE = "-" * 40


class Product:
    '''Represents and manages a single product in the inventory'''

    def __init__(self, product_id: str, name: str, price: float, stock: int, transaction_history: list[int] | None = None) -> None:
        '''Creates a product, the starting stock becomes the first transaction if no history is given.
        transaction_history parameter is of either list[int] or None type, and = None makes it optional
        parameter instead of a required one so newly added products won't crash. For newly added products =None
        makes transaction_history=None when no transaction_history parameter is passed, such as for newly added products.'''

        self.__product_id: str = product_id
        self.__name: str = name
        self.__price: float = price
        self.__stock: int = stock

        self.__transaction_history: list[int]
        if transaction_history is None:
            self.__transaction_history = [stock]
        else:
            self.__transaction_history = list(transaction_history)

    def get_product_id(self) -> str:
        '''Returns the product id'''
        return self.__product_id

    def get_name(self) -> str:
        '''Returns the product name'''
        return self.__name

    def get_price(self) -> float:
        '''Returns the product price'''
        return self.__price

    def get_stock(self) -> int:
        '''Returns the current stock quantity'''
        return self.__stock

    def get_transaction_history(self) -> list[int]:
        '''Returns a copy of the transaction history'''
        # return a copy so code outside the class cannot change the history without going through update_stock
        return list(self.__transaction_history)

    def update_stock(self, quantity: int) -> None:
        '''Replaces the stock with a new quantity and records the change in the transaction history'''
        # the product controls its own stock so it refuses a value that would put it in an invalid state
        if quantity < 0:
            raise ValueError("Stock quantity cannot be negative.")

        # record how much the stock changed: positive for a delivery, negative for a sale
        # so the full history of transactions is kept, not just the running total
        change = quantity - self.__stock
        if change != 0:
            self.__transaction_history.append(change)

        self.__stock = quantity

    def display_information(self) -> None:
        '''Prints the id, name, price and stock on one line'''
        print(f"ID: {self.__product_id} | Name: {self.__name} | Price: ${self.__price:.2f} | Stock: {self.__stock}")

    def display_details(self) -> None:
        '''Prints every detail of the product on its own line'''
        print(DIVIDER_LINE)
        print(f"ID: {self.__product_id}")
        print(f"Name: {self.__name}")
        print(f"Price: ${self.__price:.2f}")
        print(f"Stock: {self.__stock}")
        print(DIVIDER_LINE)
