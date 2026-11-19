from DiscountStrategy import DiscountStrategy


class BulkDiscount(DiscountStrategy):

    def __init__(self, threshold: float, amount: float) -> None:
        if threshold <= 0:
            raise ValueError("Threshold must be greater than zero.")
        if amount <= 0:
            raise ValueError("Discount amount must be greater than zero.")
        if amount > threshold:
            raise ValueError("Discount amount cannot be more than the threshold.")

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
