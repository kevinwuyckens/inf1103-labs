from Supplier import Supplier
from PhysicalProduct import PhysicalProduct
from Inventory import Inventory


def main() -> None:
    supplier = Supplier("S001", "Gadget Hub Supplies", "sales@gadgethub.example.com")
    mouse = PhysicalProduct("P002", "Wireless Mouse", 25.50, 40, supplier, 0.1)

    inventory_a = Inventory()
    inventory_b = Inventory()
    inventory_a.add_product(mouse)

    print("Aggregation: Inventory and Product")
    print("\nInventory A before removing P002:")
    inventory_a.display_all()

    removed = inventory_a.remove_product("P002")

    print("\nInventory A after removing P002:")
    inventory_a.display_all()
    print(f"remove_product() returned the same mouse: {removed is mouse}")

    mouse.update_stock(35)
    print(f"The mouse still works: stock {mouse.get_stock()}, history {mouse.get_transaction_history()}")

    inventory_b.add_product(mouse)
    print(f"Inventory B now holds the same mouse: {inventory_b.find_product('P002') is mouse}")


if __name__ == "__main__":
    main()
