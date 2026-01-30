import csv
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
FILE_NAME = os.path.join(BASE_DIR, "catalog.csv")
HEADERS = ["id", "name", "description"]


def load_items():
    items = []

    if not os.path.exists(FILE_NAME):
        with open(FILE_NAME, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(HEADERS)
        return items

    with open(FILE_NAME, "r", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["id"]:
                items.append({
                    "id": int(row["id"]),
                    "name": row["name"],
                    "description": row["description"]
                })
    return items


def save_items(items):
    with open(FILE_NAME, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=HEADERS)
        writer.writeheader()
        for item in items:
            writer.writerow({
                "id": item["id"],
                "name": item["name"],
                "description": item["description"]
            })


def show_items(items):
    if not items:
        print("\nNo items found.\n")
        return

    for item in items:
        print(f"\nID: {item['id']}")
        print(f"Name: {item['name']}")
        print(f"Description: {item['description']}")
        print("-" * 30)


def add_item(items):
    name = input("Enter name: ").strip()
    description = input("Enter description: ").strip()

    if not name or not description:
        print("Name and description cannot be empty.")
        return

    new_id = max([item["id"] for item in items], default=0) + 1

    items.append({
        "id": new_id,
        "name": name,
        "description": description
    })

    print("Item added!")


def edit_item(items):
    show_items(items)

    try:
        item_id = int(input("Enter ID to edit: "))
    except ValueError:
        print("Invalid ID.")
        return

    for item in items:
        if item["id"] == item_id:
            new_name = input(f"New name ({item['name']}): ").strip()
            new_desc = input(f"New description ({item['description']}): ").strip()

            if new_name:
                item["name"] = new_name
            if new_desc:
                item["description"] = new_desc

            print("Item updated!")
            return

    print("Item not found.")


def main():
    items = load_items()

    while True:
        print("\n1. View items")
        print("2. Add item")
        print("3. Edit item")
        print("4. Save and Exit")

        choice = input("Choose (1-4): ")

        if choice == "1":
            show_items(items)
        elif choice == "2":
            add_item(items)
        elif choice == "3":
            edit_item(items)
        elif choice == "4":
            save_items(items)
            print("Saved. Goodbye!")
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
