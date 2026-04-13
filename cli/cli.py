import requests

BASE_URL = "http://127.0.0.1:5000"

def print_menu():
    print("\n========================================")
    print("     INVENTORY MANAGEMENT SYSTEM CLI    ")
    print("========================================")
    print("1. View all inventory items")
    print("2. View single item")
    print("3. Add new item")
    print("4. Update item")
    print("5. Delete item")
    print("6. Fetch product by barcode (OpenFoodFacts)")
    print("7. Search product by name (OpenFoodFacts)")
    print("8. Fetch from OpenFoodFacts and add to inventory")
    print("0. Exit")
    print("========================================")

def view_all():
    response = requests.get(f"{BASE_URL}/items/")
    items = response.json()
    if not items:
        print("\nNo items in inventory.")
        return
    print("\n--- All Inventory Items ---")
    for item in items:
        print(f"\n  ID       : {item['id']}")
        print(f"  Name     : {item['name']}")
        print(f"  Brand    : {item['brand']}")
        print(f"  Price    : ${item['price']}")
        print(f"  Quantity : {item['quantity']}")
        print(f"  Barcode  : {item['barcode']}")

def view_one():
    item_id  = input("Enter item ID: ")
    response = requests.get(f"{BASE_URL}/items/{item_id}")
    if response.status_code == 404:
        print("Item not found.")
        return
    item = response.json()
    print(f"\n  ID       : {item['id']}")
    print(f"  Name     : {item['name']}")
    print(f"  Brand    : {item['brand']}")
    print(f"  Price    : ${item['price']}")
    print(f"  Quantity : {item['quantity']}")
    print(f"  Barcode  : {item['barcode']}")

def add_item():
    print("\n--- Add New Item ---")
    name        = input("Name: ")
    description = input("Description: ")
    price       = float(input("Price: "))
    quantity    = int(input("Quantity: "))
    brand       = input("Brand (optional): ")
    barcode     = input("Barcode (optional): ")
    data = {
        "name": name, "description": description,
        "price": price, "quantity": quantity,
        "brand": brand, "barcode": barcode,
    }
    response = requests.post(f"{BASE_URL}/items/", json=data)
    if response.status_code == 201:
        print(f"\nItem '{name}' added successfully!")
    else:
        print(f"\nError: {response.json().get('error')}")

def update_item():
    print("\n--- Update Item ---")
    item_id  = input("Enter item ID to update: ")
    data     = {}
    name     = input("New name (Enter to skip): ")
    price    = input("New price (Enter to skip): ")
    quantity = input("New quantity (Enter to skip): ")
    if name:     data["name"]     = name
    if price:    data["price"]    = float(price)
    if quantity: data["quantity"] = int(quantity)
    response = requests.patch(f"{BASE_URL}/items/{item_id}", json=data)
    if response.status_code == 200:
        print("\nItem updated successfully!")
    else:
        print(f"\nError: {response.json().get('error')}")

def delete_item():
    print("\n--- Delete Item ---")
    item_id  = input("Enter item ID to delete: ")
    response = requests.delete(f"{BASE_URL}/items/{item_id}")
    if response.status_code == 200:
        print(f"\n{response.json().get('message')}")
    else:
        print(f"\nError: {response.json().get('error')}")

def fetch_by_barcode():
    print("\n--- Fetch by Barcode ---")
    barcode  = input("Enter barcode: ")
    response = requests.get(f"{BASE_URL}/external/barcode/{barcode}")
    if response.status_code == 200:
        product = response.json()
        print(f"\n  Name        : {product['name']}")
        print(f"  Brand       : {product['brand']}")
        print(f"  Description : {product['description']}")
        print(f"  Barcode     : {product['barcode']}")
    else:
        print(f"\nError: {response.json().get('error')}")

def search_by_name():
    print("\n--- Search by Name ---")
    name     = input("Enter product name: ")
    response = requests.get(f"{BASE_URL}/external/search", params={"name": name})
    if response.status_code == 200:
        results = response.json()
        print(f"\nFound {len(results)} products:")
        for p in results:
            print(f"\n  Name    : {p['name']}")
            print(f"  Brand   : {p['brand']}")
            print(f"  Barcode : {p['barcode']}")
    else:
        print(f"\nError: {response.json().get('error')}")

def fetch_and_add():
    print("\n--- Fetch from OpenFoodFacts and Add to Inventory ---")
    barcode  = input("Enter barcode: ")
    price    = float(input("Enter price: "))
    quantity = int(input("Enter quantity: "))
    response = requests.post(
        f"{BASE_URL}/external/barcode/{barcode}/add",
        json={"price": price, "quantity": quantity}
    )
    if response.status_code == 201:
        item = response.json()["item"]
        print(f"\nProduct '{item['name']}' added to inventory successfully!")
    else:
        print(f"\nError: {response.json().get('error')}")

def main():
    print("\nWelcome to the Inventory Management System")
    while True:
        print_menu()
        choice = input("\nEnter your choice: ")
        if   choice == "1": view_all()
        elif choice == "2": view_one()
        elif choice == "3": add_item()
        elif choice == "4": update_item()
        elif choice == "5": delete_item()
        elif choice == "6": fetch_by_barcode()
        elif choice == "7": search_by_name()
        elif choice == "8": fetch_and_add()
        elif choice == "0":
            print("\nGoodbye!")
            break
        else:
            print("\nInvalid choice. Please try again.")

if __name__ == "__main__":
    main()
