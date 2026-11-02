from abc import ABC, abstractmethod


class CanBeShipped(ABC):

    @abstractmethod
    def calculate_shipping_cost(self) -> float:
        '''Every class that implements CanBeShipped must provide a way to calculate its shipping cost'''
        pass
