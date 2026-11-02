from Product import Product


class DigitalProduct(Product):

    def __init__(self, product_id: str, name: str, price: float, stock: int, download_size: float, transaction_history: list[int] | None = None) -> None:
        super().__init__(product_id, name, price, stock, transaction_history)
        self.__download_size: float = download_size

    def get_download_size(self) -> float:
        return self.__download_size

    def display_information(self) -> None:
        super().display_information()
        print(f"Type: Digital | Download Size: {self.__download_size:.2f} MB")

    def display_details(self) -> None:
        super().display_details()
        print("Type: Digital")
        print(f"Download Size: {self.__download_size:.2f} MB")

    def get_fulfilment_info(self) -> str:
        return "This product is delivered digitally through a download link."

    def to_dictionary(self) -> dict:
        data = super().to_dictionary()
        data["type"] = "digital"
        data["download_size"] = self.__download_size
        return data
