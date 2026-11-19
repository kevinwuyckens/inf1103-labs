from Product import Product


class OrderLine:

    def __init__(self, product: Product, quantity: int) -> None:
        if quantity <= 0:
            raise ValueError("Order quantity must be greater than 0.")

        self.__product: Product = product
        self.__quantity: int = quantity

    def get_product(self) -> Product:
        return self.__product

    def get_quantity(self) -> int:
        return self.__quantity

    def calculate_subtotal(self) -> float:
        return self.__product.get_price() * self.__quantity

    def display_information(self) -> None:
        print(f"{self.__product.get_product_id()} | {self.__product.get_name()} | "
              f"${self.__product.get_price():.2f} x {self.__quantity} = ${self.calculate_subtotal():.2f}")
