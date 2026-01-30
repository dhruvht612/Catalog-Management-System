"""
============================================================================
CATALOG MANAGEMENT SYSTEM - Python CLI Version
============================================================================
Architecture:
- Frontend: Command-Line Interface (CLI) - user interaction layer
- Backend: Python business logic - data processing and validation
- Database: CSV file (catalog.csv) - flat-file database storage
============================================================================
"""

import csv
import os
from typing import List, Dict, Optional

# Database Configuration
CSV_FILE = 'catalog.csv'
CSV_HEADERS = ['id', 'name', 'description']

# ============================================================================
# DATABASE LAYER: CSV File Operations
# ============================================================================

def load_items() -> List[Dict[str, str]]:
    """
    Database Operation: Read all items from CSV file
    - Frontend: Not directly called by user, used by backend
    - Backend: Retrieves data from database
    - Database: Reads from catalog.csv (simulates SELECT * FROM items)
    
    Returns:
        List of dictionaries, each representing a catalog item
    """
    items = []
    
    # Database: Check if file exists (simulates database connection check)
    if not os.path.exists(CSV_FILE):
        print(f"Database file '{CSV_FILE}' not found. Creating new database...")
        # Database: Create file with headers (simulates CREATE TABLE)
        with open(CSV_FILE, 'w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=CSV_HEADERS)
            writer.writeheader()
        return items
    
    # Database: Read from CSV file (simulates SQL SELECT query)
    try:
        with open(CSV_FILE, 'r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            items = []
            
            # Backend: Read and process each row, filtering out empty rows
            for row in reader:
                # Filter out empty rows (rows where id is empty or None)
                if row.get('id') and row['id'].strip():
                    try:
                        # Backend: Convert id to integer for proper sorting
                        row['id'] = int(row['id'].strip())
                        # Ensure name and description are not None
                        row['name'] = row.get('name', '').strip()
                        row['description'] = row.get('description', '').strip()
                        items.append(row)
                    except ValueError:
                        # Skip rows with invalid ID
                        continue
            
            # Backend: Sort items by ID for consistent display
            items.sort(key=lambda x: x['id'])
            
            print(f"Database: Loaded {len(items)} items from {CSV_FILE}")
            return items
    except Exception as e:
        print(f"Database Error: Failed to read {CSV_FILE}: {e}")
        return []


def save_items(items: List[Dict[str, str]]) -> bool:
    """
    Database Operation: Write all items to CSV file
    - Frontend: Not directly called by user, used by backend
    - Backend: Persists data to database
    - Database: Writes to catalog.csv (simulates UPDATE/INSERT operations)
    
    Args:
        items: List of item dictionaries to save
        
    Returns:
        True if successful, False otherwise
    """
    try:
        # Database: Write to CSV file (simulates SQL INSERT/UPDATE)
        with open(CSV_FILE, 'w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=CSV_HEADERS)
            writer.writeheader()
            
            # Backend: Convert id back to string for CSV storage
            for item in items:
                item_copy = item.copy()
                item_copy['id'] = str(item_copy['id'])
                writer.writerow(item_copy)
        
        print(f"Database: Saved {len(items)} items to {CSV_FILE}")
        return True
    except Exception as e:
        print(f"Database Error: Failed to save to {CSV_FILE}: {e}")
        return False


# ============================================================================
# BACKEND LAYER: Business Logic and Validation
# ============================================================================

def validate_input(name: str, description: str) -> bool:
    """
    Backend: Input validation
    - Frontend: Called when user submits form data
    - Backend: Validates business rules (fields must not be empty)
    - Database: Not involved in validation
    
    Args:
        name: Item name to validate
        description: Item description to validate
        
    Returns:
        True if valid, False otherwise
    """
    # Backend: Validate name field
    if not name or not name.strip():
        print("Backend Validation Error: Name field cannot be empty")
        return False
    
    # Backend: Validate description field
    if not description or not description.strip():
        print("Backend Validation Error: Description field cannot be empty")
        return False
    
    return True


def get_next_id(items: List[Dict[str, str]]) -> int:
    """
    Backend: Generate next available ID
    - Frontend: Not directly called
    - Backend: Business logic for ID generation
    - Database: Simulates AUTO_INCREMENT in database
    
    Args:
        items: Current list of items
        
    Returns:
        Next available ID number
    """
    if not items:
        return 1
    
    # Backend: Find maximum ID and increment (simulates database AUTO_INCREMENT)
    max_id = max(item['id'] for item in items if isinstance(item['id'], int))
    return max_id + 1


def find_item_by_id(items: List[Dict[str, str]], item_id: int) -> Optional[Dict[str, str]]:
    """
    Backend: Find item by ID
    - Frontend: Called when user selects item to edit/view
    - Backend: Searches in-memory data structure
    - Database: Simulates SELECT * FROM items WHERE id = ?
    
    Args:
        items: List of items to search
        item_id: ID to search for
        
    Returns:
        Item dictionary if found, None otherwise
    """
    for item in items:
        if item['id'] == item_id:
            return item
    return None


# ============================================================================
# FRONTEND LAYER: CLI User Interface
# ============================================================================

def display_items(items: List[Dict[str, str]]) -> None:
    """
    Frontend: Display all items in CLI
    - Frontend: Renders data for user viewing
    - Backend: Formats data for display
    - Database: Data already loaded in memory
    
    Args:
        items: List of items to display
    """
    if not items:
        print("\n" + "="*60)
        print("No items in catalog. Add your first item!")
        print("="*60 + "\n")
        return
    
    print("\n" + "="*60)
    print("CATALOG ITEMS")
    print("="*60)
    
    # Frontend: Format and display each item
    for item in items:
        print(f"\nID: {item['id']}")
        print(f"Name: {item['name']}")
        print(f"Description: {item['description']}")
        print("-" * 60)
    
    print(f"\nTotal items: {len(items)}\n")


def display_item_details(item: Dict[str, str]) -> None:
    """
    Frontend: Display single item details
    - Frontend: Shows detailed view of one item
    - Backend: Formats item data
    - Database: Item already retrieved from memory
    
    Args:
        item: Item dictionary to display
    """
    print("\n" + "="*60)
    print("ITEM DETAILS")
    print("="*60)
    print(f"ID: {item['id']}")
    print(f"Name: {item['name']}")
    print(f"Description: {item['description']}")
    print("="*60 + "\n")


def add_item(items: List[Dict[str, str]]) -> None:
    """
    Frontend + Backend: Add new item to catalog
    - Frontend: Prompts user for input via CLI
    - Backend: Validates input and processes addition
    - Database: Item will be saved when save_items() is called
    
    Args:
        items: Current list of items (modified in place)
    """
    print("\n" + "="*60)
    print("ADD NEW ITEM")
    print("="*60)
    
    # Frontend: Get user input via CLI
    name = input("Enter item name: ").strip()
    description = input("Enter item description: ").strip()
    
    # Backend: Validate input
    if not validate_input(name, description):
        print("Item not added. Please fix the errors above.")
        return
    
    # Backend: Generate ID and create new item
    new_id = get_next_id(items)
    new_item = {
        'id': new_id,
        'name': name,
        'description': description
    }
    
    # Backend: Add to in-memory data structure
    items.append(new_item)
    
    print(f"\nFrontend: Item added successfully!")
    print(f"Backend: Created item with ID {new_id}")
    print(f"Database: Item will be saved when you choose 'Save and Exit'\n")


def edit_item(items: List[Dict[str, str]]) -> None:
    """
    Frontend + Backend: Edit existing item
    - Frontend: Prompts user for item ID and new data via CLI
    - Backend: Validates input and processes update
    - Database: Changes will be saved when save_items() is called
    
    Args:
        items: Current list of items (modified in place)
    """
    if not items:
        print("\nNo items to edit. Add items first.\n")
        return
    
    print("\n" + "="*60)
    print("EDIT ITEM")
    print("="*60)
    
    # Frontend: Display items for reference
    display_items(items)
    
    # Frontend: Get item ID from user
    try:
        item_id = int(input("Enter the ID of the item to edit: ").strip())
    except ValueError:
        print("Invalid ID. Please enter a number.")
        return
    
    # Backend: Find item
    item = find_item_by_id(items, item_id)
    
    if not item:
        print(f"Item with ID {item_id} not found.")
        return
    
    # Frontend: Show current item details
    print("\nCurrent item details:")
    display_item_details(item)
    
    # Frontend: Get new data from user
    print("Enter new values (press Enter to keep current value):")
    new_name = input(f"Name [{item['name']}]: ").strip()
    new_description = input(f"Description [{item['description']}]: ").strip()
    
    # Backend: Use new values or keep existing
    if new_name:
        item['name'] = new_name
    if new_description:
        item['description'] = new_description
    
    # Backend: Validate updated data
    if not validate_input(item['name'], item['description']):
        print("Item not updated. Please fix the errors above.")
        return
    
    print(f"\nFrontend: Item updated successfully!")
    print(f"Backend: Updated item with ID {item_id}")
    print(f"Database: Changes will be saved when you choose 'Save and Exit'\n")


def display_menu() -> None:
    """
    Frontend: Display main menu options
    - Frontend: CLI menu interface
    - Backend: Not involved
    - Database: Not involved
    """
    print("\n" + "="*60)
    print("CATALOG MANAGEMENT SYSTEM")
    print("="*60)
    print("1. View all items")
    print("2. Add item")
    print("3. Edit item")
    print("4. Save and Exit")
    print("="*60)


# ============================================================================
# MAIN APPLICATION LOOP
# ============================================================================

def main():
    """
    Main application entry point
    Coordinates Frontend (CLI), Backend (logic), and Database (CSV) layers
    """
    print("="*60)
    print("CATALOG MANAGEMENT SYSTEM - Python CLI Version")
    print("="*60)
    print("Architecture:")
    print("  Frontend: Command-Line Interface (CLI)")
    print("  Backend: Python business logic")
    print("  Database: CSV file (catalog.csv)")
    print("="*60)
    
    # Database: Load items from CSV file
    items = load_items()
    
    # Main application loop (Frontend: CLI interaction)
    while True:
        display_menu()
        
        # Frontend: Get user choice
        choice = input("\nEnter your choice (1-4): ").strip()
        
        # Frontend + Backend: Process user choice
        if choice == '1':
            # Frontend: Display all items
            display_items(items)
        elif choice == '2':
            # Frontend + Backend: Add new item
            add_item(items)
        elif choice == '3':
            # Frontend + Backend: Edit existing item
            edit_item(items)
        elif choice == '4':
            # Database: Save all changes to CSV file
            if save_items(items):
                print("\n" + "="*60)
                print("All changes saved successfully!")
                print("Thank you for using Catalog Management System.")
                print("="*60 + "\n")
            else:
                print("\nError: Failed to save changes. Please try again.")
            break
        else:
            # Frontend: Invalid choice handling
            print("\nInvalid choice. Please enter 1, 2, 3, or 4.")


# Entry point
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nProgram interrupted by user.")
        print("Warning: Unsaved changes will be lost!")
        print("Use option 4 to save before exiting.")
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        print("Please report this error to the developer.")
