from Product import Product


class PhysicalProduct(Product):

    def __init__(self, product_id: str, name: str, price: float, stock: int, weight: float, transaction_history: list[int] | None = None) -> None:
        super().__init__(product_id, name, price, stock, transaction_history)
        self.__weight: float = weight

    def get_weight(self) -> float:
        return self.__weight

    def display_information(self) -> None:
        super().display_information()
        print(f"    Type: Physical | Weight: {self.__weight:.2f} kg")

    def display_details(self) -> None:
        super().display_details()
        print("Type: Physical")
        print(f"Weight: {self.__weight:.2f} kg")
