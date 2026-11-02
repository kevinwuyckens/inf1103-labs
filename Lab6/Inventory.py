from Product import Product

DIVIDER_LINE = "-" * 40


class Inventory:
    '''Manages a collection of Product objects'''

    def __init__(self) -> None:
        '''Creates an empty inventory'''
        self.__products: list[Product] = []

    def add_product(self, product: Product) -> bool:
        '''Adds a product to the inventory, returns False if a product with the same id already exists'''
        # product id must be unique otherwise search and update would not know which product to use
        if self.search_product(product.get_product_id()) is not None:
            return False

        self.__products.append(product)
        return True

    def search_product(self, product_id: str) -> Product | None:
        '''Returns the product with the matching product_id, or None if it is not in the inventory'''
        for product in self.__products:
            if product.get_product_id() == product_id:
                return product
        return None

    def get_products(self) -> list[Product]:
        '''Returns a copy of the list of products'''
        # return a copy so code outside the class cannot add or remove products without going through add_product
        return list(self.__products)

    def display_all(self) -> None:
        '''Prints the id, name, price and stock of every product in the inventory'''
        print("\nCurrent Inventory")
        print(DIVIDER_LINE)

        if len(self.__products) == 0:
            print("No products in inventory.")

        # each product knows how to display itself
        for product in self.__products:
            product.display_information()

        print(DIVIDER_LINE)
