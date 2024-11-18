import json
from patron import Patron
from library_item import Book, Magazine, DVD, LibraryItem
from staff_assignment import load_staff_assignment_from_file

# Load the staff_assignment data from file
staff_assignment = load_staff_assignment_from_file('staff_assignment.txt')

# Load the staff_assignment.txt data
def save_staff_assignment(data):
    try:
        with open("staff_assignment.txt", "w") as file:
            json.dump(data, file, indent=4)
    except Exception as e:
        print(f"Error saving data: {e}")

# Function to search for an item
def search_item(item_type, title):
    global staff_assignment  # Use the globally loaded staff_assignment variable

    # Check if the item type exists
    if item_type not in staff_assignment:
        print(f"No items of type '{item_type}' found.")
        return False

    # Check if the title exists within the given item type
    if title in staff_assignment[item_type]:
        item_info = staff_assignment[item_type][title]
        staff = item_info.get("staff")
        station = item_info.get("station")
        
        # Display general information
        print(f"'{title}' ({item_type}) is available.")
        print(f"Assigned to staff: {staff}, Station: {station}")

        # Additional details based on item type
        if item_type == "Book":
            author = item_info.get("author")
            genre = item_info.get("genre")
            print(f"Author: {author}, Genre: {genre}")
        
        elif item_type == "Magazine":
            issue = item_info.get("issue")
            print(f"Issue: {issue}")

        elif item_type == "DVD":
            director = item_info.get("director")
            genre = item_info.get("genre")
            print(f"Director: {director}, Genre: {genre}")
        
        return True

    else:
        print(f"'{title}' ({item_type}) is not available.")
        return False

def borrow_or_return_item(patron):
    global staff_assignment  # Use the globally loaded staff_assignment variable

    while True:
        item_type = input("\nWhat type of item would you like to search for? (Book/Magazine/DVD): ").strip()

        if item_type not in staff_assignment:
            print("Invalid item type selected.")
            continue

        title = input(f"Enter the title of the {item_type}: ").strip()

        if not search_item(item_type, title):
            continue

        action = input("Would you like to borrow or return this item? (borrow/return): ").strip().lower()

        if action not in ["borrow", "return"]:
            print("Invalid action.")
            continue

        # Retrieve item data and additional attributes
        item_data = staff_assignment[item_type][title]
        publication_year = item_data.get("publication_year", "Unknown")
        language = item_data.get("language", "English")
        shelf_location = item_data.get("shelf_location", "General")
        condition = item_data.get("condition", "Good")

        # Initialize the item based on type
        if item_type == "Book":
            item = Book(title, item_data.get("author"), item_data.get("genre"),
                        item_data.get("ISBN", "N/A"), item_data.get("pages", 0),
                        publication_year, language, shelf_location, condition)
        elif item_type == "Magazine":
            item = Magazine(title, item_data.get("issue"),
                            item_data.get("issue_number", 0),
                            publication_year, language, shelf_location, condition)
        elif item_type == "DVD":
            item = DVD(title, item_data.get("director"), item_data.get("genre"),
                       item_data.get("duration", 0),
                       publication_year, language, shelf_location, condition)

        # Perform borrow or return action
        if action == "borrow":
            if item.available:
                patron.borrow_item(item)
                
                # Decrease the count in staff_assignment
                if title in staff_assignment[item_type]:
                    staff_assignment[item_type][title]['count'] -= 1
                    save_staff_assignment(staff_assignment)
                    
                    # Display updated count of remaining items for the title
                    print(f"\nUpdated {item_type} '{title}' count after borrowing: {staff_assignment[item_type][title]['count']} remaining.")
            else:
                print(f"{item_type} '{title}' is currently unavailable.")
        elif action == "return":
            patron.return_item(item)
            
            # Increase the count in staff_assignment
            if title in staff_assignment[item_type]:
                staff_assignment[item_type][title]['count'] += 1
                save_staff_assignment(staff_assignment)
                
                # Display updated count of remaining items for the title
                print(f"\nUpdated {item_type} '{title}' count after returning: {staff_assignment[item_type][title]['count']} remaining.")
        
        # Display the number of remaining copies per title in the item type
        print("\nUpdated availability per title:")
        for title, details in staff_assignment[item_type].items():
            print(f"{title}: {details['count']} remaining")
        
        another_action = input("Would you like to search for another item? (yes/no): ").strip().lower()
        if another_action != "yes":
            patron.save_patron_data()
            print("Thank you for using the library system!")
            break

# Use the new class method to display all items in the library
def display_all_items():
    all_items = LibraryItem.get_all_items()
    for item_type, items in all_items.items():
        print(f"\n{item_type}s in Library:")
        for title, details in items.items():
            print(f" - {title}")

if __name__ == '__main__':
    # Initialize item count based on staff_assignment or previous run
    LibraryItem.initialize_item_count()
    print(f"The Library has {LibraryItem._item_count} available items")

    # Main script
    user_name = input("Please enter your name: ").strip()

    # Load the patron's data if it exists
    patron = Patron.load_patron_data(user_name)

    # Display all items in the library for the user
    print("\nLibrary Catalog:")
    display_all_items()

    # Start the borrowing/returning process
    borrow_or_return_item(patron)

    # Save the patron's data when done
    patron.save_patron_data()
