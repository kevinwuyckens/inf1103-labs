from DiscountStrategy import DiscountStrategy


class PercentageDiscount(DiscountStrategy):

    def __init__(self, percentage: float) -> None:
        if percentage <= 0 or percentage > 100:
            raise ValueError("Percentage must be greater than zero and no more than 100.")

        self.__percentage: float = percentage

    def get_percentage(self) -> float:
        return self.__percentage

    def apply(self, total: float) -> float:
        return total - total * self.__percentage / 100
