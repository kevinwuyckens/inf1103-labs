from DiscountStrategy import DiscountStrategy

STUDENT_DISCOUNT_PERCENTAGE = 5


class StudentDiscount(DiscountStrategy):

    def apply(self, total: float) -> float:
        return total - total * STUDENT_DISCOUNT_PERCENTAGE / 100
