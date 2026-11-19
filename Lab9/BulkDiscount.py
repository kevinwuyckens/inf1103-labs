from DiscountStrategy import DiscountStrategy


class BulkDiscount(DiscountStrategy):

    def __init__(self, threshold: float, amount: float) -> None:
        self.__threshold: float = threshold
        self.__amount: float = amount

    def get_threshold(self) -> float:
        return self.__threshold

    def get_amount(self) -> float:
        return self.__amount

    def apply(self, total: float) -> float:
        if total >= self.__threshold:
            return total - self.__amount
        return total
