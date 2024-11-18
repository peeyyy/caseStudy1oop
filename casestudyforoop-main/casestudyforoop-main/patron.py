import json
import datetime
from borrowing_data import append_borrowing_data, delete_borrowing_data, return_append_return_data
from library_item import Book, Magazine, DVD
from staff_assignment import staff_assignment

class Patron:
    patrons_data_file = 'patrons_data.json'  # File to store patron data
    patron_count = 0  # Track total patrons in the system

    def __init__(self, name):
        """Initialize a Patron with a unique name and load or increment the count."""
        self.__name = name
        self.checked_out_items = []  # Holds checked-out LibraryItem objects for the patron
        self.borrowed_count = 0  # Tracks the count of items the patron has borrowed
        self.load_patron_count()

        # If this patron is new, increase the overall patron count
        if not self.is_existing_patron():
            Patron.patron_count += 1

    def load_patron_count(self):
        """Load total number of patrons from the data file if it exists."""
        try:
            with open(Patron.patrons_data_file, 'r') as file:
                patrons_data = json.load(file)
                if 'patron_count' in patrons_data:
                    Patron.patron_count = patrons_data['patron_count']
        except FileNotFoundError:
            Patron.patron_count = 0  # Initialize count to 0 if file not found

    def is_existing_patron(self):
        """Check if this patron exists in the saved data."""
        try:
            with open(Patron.patrons_data_file, 'r') as file:
                patrons_data = json.load(file)
                return self.__name in patrons_data
        except FileNotFoundError:
            return False  # File not found implies a new patron

    def borrow_item(self, item):
        """Allows the patron to borrow an item if it’s available."""
        item_already_borrowed = any(
            i._title == item._title and i._item_type == item._item_type for i in self.checked_out_items
        )

        # Check if patron has already borrowed this item
        if item_already_borrowed:
            print(f"{self.__name} has already borrowed '{item._title}'. Cannot borrow the same item twice.")
            return #Exit the function if the item is already borrowed

        if len(self.checked_out_items) < Patron.max_items_allowed():
            if item.available:
                # Load staff info for the item type
                staff_info = staff_assignment[item._item_type][item._title]
                staff_name = staff_info["staff"]
                staff_station = staff_info["station"]
                item.check_out()  # Check out the item and mark it unavailable
                self.checked_out_items.append(item)  # Add to patron’s items
                self.borrowed_count += 1  # Update borrowed count

                print(f"\n{self.__name} borrowed a {item._item_type}.")
                print(item)
                print(f"This {item._item_type} is handled by {staff_name} at station {staff_station}. Please proceed to check out.\n")

                # Log borrowing with due date
                date_borrowed = datetime.date.today()
                due_date = date_borrowed + datetime.timedelta(days=30)
                append_borrowing_data(self.__name, item._title, date_borrowed, due_date, item._item_type)
            else:
                print(f'{item._item_type} is not available.')
        else:
            print(f'{self.__name} has reached the max limit of borrowed items.')

    def return_item(self, item):
        """Allows the patron to return a borrowed item."""
        item_found = any(i._title == item._title and i._item_type == item._item_type for i in self.checked_out_items)

        if item_found:
            item.return_item()  # Mark item as returned and update availability
            # Remove from patron’s checked out items
            self.checked_out_items = [i for i in self.checked_out_items if not (i._title == item._title and i._item_type == item._item_type)]

            self.borrowed_count -= 1  # Update the borrowed count
            print(f'{self.__name} returned a {item._item_type}.')
            
            date_borrowed = datetime.date.today()
            due_date = date_borrowed + datetime.timedelta(days=30)
            date_return = datetime.date.today()
            return_type = 'ON TIME' if date_return <= due_date else 'OVERDUE'
            
            delete_borrowing_data(self.__name, item._title, item._item_type)  # Remove entry from borrowing data
            return_append_return_data(self.__name, item._title, date_borrowed, due_date, date_return, return_type, item._item_type)
        else:
            print(f'\n{self.__name} does not have {item._item_type} checked out.')

    @classmethod
    def total_patrons(cls):
        """Returns the total count of patrons."""
        return cls.patron_count

    @staticmethod
    def max_items_allowed():
        """Defines the maximum allowed items a patron can borrow."""
        return 5

    def save_patron_data(self):
        """Save patron's checked out items and update the patron data file."""
        try:
            with open(Patron.patrons_data_file, 'r') as file:
                patrons_data = json.load(file)
        except FileNotFoundError:
            patrons_data = {}

        # Update patron's data with current checked out items
        patrons_data[self.__name] = [{
            "title": item._title, 
            "type": item._item_type,
            "publication_year": item.publication_year,
            "language": item.language,
            "shelf_location": item.shelf_location,
            "condition": item.condition
        } for item in self.checked_out_items]

        # Order data and save patron count
        ordered_data = {'patron_count': Patron.patron_count}

        for patron in patrons_data:
            if patron != 'patron_count':  # Ensure patron count is added first
                ordered_data[patron] = patrons_data[patron]

        with open(Patron.patrons_data_file, 'w') as file:
            json.dump(ordered_data, file, indent=4)

    @classmethod
    def load_patron_data(cls, name):
        """Load patron’s saved data and checked-out items if they exist."""
        try:
            with open(cls.patrons_data_file, 'r') as file:
                patrons_data = json.load(file)
                
                if name in patrons_data:
                    patron = cls(name)
                    
                    for item_data in patrons_data[name]:
                        title = item_data["title"]
                        item_type = item_data["type"]
                        publication_year = item_data.get("publication_year", "Unknown")
                        language = item_data.get("language", "English")
                        shelf_location = item_data.get("shelf_location", "General")
                        condition = item_data.get("condition", "Good")
                        
                        # Initialize the item based on its type
                        if item_type == "Book":
                            item = Book(title, "Unknown Author", "Unknown Genre", "N/A", 0,
                                        publication_year, language, shelf_location, condition)
                        elif item_type == "Magazine":
                            item = Magazine(title, "Unknown Issue", 0,
                                            publication_year, language, shelf_location, condition)
                        elif item_type == "DVD":
                            item = DVD(title, "Unknown Director", "Unknown Genre", 0,
                                       publication_year, language, shelf_location, condition)
                        else:
                            print(f"Unknown item type: {item_type}.")
                            continue #Skip unknown item types
                        
                        patron.checked_out_items.append(item)
                    return patron

        except FileNotFoundError:
            print("Patron data file not found. A new patron will be created.")
        except json.JSONDecodeError:
            print("Error decoding JSON data. Please check the file format.")
        
        return cls(name)  # Return new patron instance if data load fails or not found