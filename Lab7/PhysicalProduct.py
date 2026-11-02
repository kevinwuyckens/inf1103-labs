from CanBeShipped import CanBeShipped
from Product import Product

BASE_SHIPPING_COST = 5.00
SHIPPING_COST_PER_KG = 2.00


class PhysicalProduct(Product, CanBeShipped):

    def __init__(self, product_id: str, name: str, price: float, stock: int, weight: float, transaction_history: list[int] | None = None) -> None:
        super().__init__(product_id, name, price, stock, transaction_history)
        self.__weight: float = weight

    def get_weight(self) -> float:
        return self.__weight

    def display_information(self) -> None:
        super().display_information()
        print(f"Type: Physical | Weight: {self.__weight:.2f} kg")

    def display_details(self) -> None:
        super().display_details()
        print("Type: Physical")
        print(f"Weight: {self.__weight:.2f} kg")

    def get_fulfilment_info(self) -> str:
        return "This product requires physical shipping to the customer's address."

    def calculate_shipping_cost(self) -> float:
        return BASE_SHIPPING_COST + SHIPPING_COST_PER_KG * self.__weight

    def to_dictionary(self) -> dict:
        data = super().to_dictionary()
        data["type"] = "physical"
        data["weight"] = self.__weight
        return data
