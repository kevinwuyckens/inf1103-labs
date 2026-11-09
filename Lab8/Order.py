from OrderLine import OrderLine
from Product import Product

DIVIDER_LINE = "-" * 40


class Order:

    def __init__(self, order_id: str) -> None:
        self.__order_id: str = order_id
        self.__order_lines: list[OrderLine] = []

    def get_order_id(self) -> str:
        return self.__order_id

    def add_order_line(self, product: Product, quantity: int) -> None:
        order_line = OrderLine(product, quantity)
        self.__order_lines.append(order_line)

    def remove_order_line(self, product_id: str) -> bool:
        for order_line in self.__order_lines:
            if order_line.get_product().get_product_id() == product_id:
                self.__order_lines.remove(order_line)
                return True
        return False

    def get_order_lines(self) -> list[OrderLine]:
        return list(self.__order_lines)

    def calculate_total(self) -> float:
        total = 0.0
        for order_line in self.__order_lines:
            total += order_line.calculate_subtotal()
        return total

    def display_information(self) -> None:
        print(f"\nOrder {self.__order_id}")
        print(DIVIDER_LINE)

        if len(self.__order_lines) == 0:
            print("No items in this order.")

        for order_line in self.__order_lines:
            order_line.display_information()

        print(DIVIDER_LINE)
        print(f"Order Total: ${self.calculate_total():.2f}")
