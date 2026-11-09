from abc import ABC, abstractmethod
from Supplier import Supplier


class Product(ABC):
    def __init__(self, product_id: str, name: str, price: float, stock: int, supplier: Supplier, transaction_history: list[int] | None = None) -> None:
        self.__product_id: str = product_id
        self.__name: str = name
        self.__price: float = price
        self.__stock: int = stock
        self.__supplier: Supplier = supplier

        self.__transaction_history: list[int]
        if transaction_history is None:
            self.__transaction_history = [stock]
        else:
            self.__transaction_history = list(transaction_history)

    def get_product_id(self) -> str:
        return self.__product_id

    def get_name(self) -> str:
        return self.__name

    def get_price(self) -> float:
        return self.__price

    def get_stock(self) -> int:
        return self.__stock

    def get_supplier(self) -> Supplier:
        return self.__supplier

    def get_transaction_history(self) -> list[int]:
        return list(self.__transaction_history)

    def update_stock(self, quantity: int) -> None:
        if quantity < 0:
            raise ValueError("Stock quantity cannot be negative.")

        change = quantity - self.__stock
        if change != 0:
            self.__transaction_history.append(change)

        self.__stock = quantity

    def display_information(self) -> None:
        print(f"ID: {self.__product_id} | Name: {self.__name} | Price: ${self.__price:.2f} | Stock: {self.__stock}")

    def display_details(self) -> None:
        print(f"ID: {self.__product_id}")
        print(f"Name: {self.__name}")
        print(f"Price: ${self.__price:.2f}")
        print(f"Stock: {self.__stock}")
        print(f"Supplier: {self.__supplier.get_name()} ({self.__supplier.get_supplier_id()})")

    def to_dictionary(self) -> dict[str, str | int | float | list[int]]:
        return {
            "id": self.__product_id,
            "name": self.__name,
            "price": self.__price,
            "stock": self.__stock,
            "supplier_id": self.__supplier.get_supplier_id(),
            "transaction_history": list(self.__transaction_history)
        }

    @abstractmethod
    def get_fulfilment_info(self) -> str:
        pass
