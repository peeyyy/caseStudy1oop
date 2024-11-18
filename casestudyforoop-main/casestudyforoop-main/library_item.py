import json
from abc import ABC, abstractmethod
from staff_assignment import staff_assignment

# Abstract base class for all library items
class LibraryItem(ABC):
    _item_count = 0  # Tracks total count of all items in the library
    _count_per_items = {}  # Holds the count of items per type
    item_count_file = 'item_count.json'  # File to persist the item count across sessions

    # Initialize common attributes for each library item
    def __init__(self, title, item_type, publication_year, language, shelf_location, condition):
        self._title = title  # Item's title
        self._item_type = item_type  # Type of item (e.g., Book, DVD, Magazine)
        self.available = True  # Availability status
        self.staff = staff_assignment[item_type][title]  # Staff member responsible for the item
        self.publication_year = publication_year  # Year the item was published
        self.language = language  # Language of the item
        self.shelf_location = shelf_location  # Location in the library
        self.condition = condition  # Condition of the item (e.g., New, Good, Worn)

    # Abstract method for checking out an item
    @abstractmethod
    def check_out(self):
        pass

    # Abstract method for returning an item
    @abstractmethod
    def return_item(self):
        pass

    # String representation of the library item
    def __str__(self):
        return f"{self._item_type} - Title: {self._title}"

    # Returns the total count of items in the library
    @staticmethod
    def total_items():
        return LibraryItem._item_count

    # Increments item count and saves the updated count to a file
    @staticmethod
    def increment_item_count(item_type, title):
        if item_type in LibraryItem._count_per_items:
            if title in LibraryItem._count_per_items[item_type]:
                # Increase the count for that specific title
                LibraryItem._count_per_items[item_type][title] += 1
                LibraryItem._item_count += 1  # Increase total item count
                LibraryItem.save_item_count()
                print(f"Title '{title}' of type '{item_type}' has been returned. Remaining copies: {LibraryItem._count_per_items[item_type][title]}")
            else:
                print(f"Title '{title}' not found in {item_type}.")
        else:
            print(f"Item type '{item_type}' not found.")

    # Decrements item count if above zero, then saves the updated count
    @staticmethod
    def decrement_item_count(item_type, title):
        if item_type in LibraryItem._count_per_items:
            if title in LibraryItem._count_per_items[item_type]:
                # Decrease the count for that specific title
                if LibraryItem._count_per_items[item_type][title] > 0:
                    LibraryItem._count_per_items[item_type][title] -= 1
                    LibraryItem._item_count -= 1  # Decrease total item count
                    LibraryItem.save_item_count()
                    print(f"Title '{title}' of type '{item_type}' has been borrowed. Remaining copies: {LibraryItem._count_per_items[item_type][title]}")
                else:
                    print(f"No copies left of '{title}' to borrow.")
            else:
                print(f"Title '{title}' not found in {item_type}.")
        else:
            print(f"Item type '{item_type}' not found.")

    # Initializes item count from the file or calculates it if the file is missing
    @staticmethod
    def initialize_item_count():
        try:
            with open(LibraryItem.item_count_file, 'r') as file:
                counts = json.load(file)
                LibraryItem._item_count = counts.get('total', 0)
                LibraryItem._count_per_items = counts['per_title']
        except (FileNotFoundError, json.JSONDecodeError):
            LibraryItem._count_per_items = {item_type: len(items) for item_type, items in staff_assignment.items()}
            LibraryItem._item_count = sum(LibraryItem._count_per_items.values())
            LibraryItem.save_item_count()

    # Saves the item count to a JSON file for persistence
    @staticmethod
    def save_item_count():
        counts = {
            'total': LibraryItem._item_count,
            'per_title': LibraryItem._count_per_items
        }
        with open(LibraryItem.item_count_file, 'w') as file:
            json.dump(counts, file)

    # Adds a new item to the staff assignment and increments the count
    @classmethod
    def add_item(cls, item_type, title, details):
        if item_type in staff_assignment:
            staff_assignment[item_type][title] = details
            cls.increment_item_count(item_type)
        else:
            print("Invalid item type.")

    # Removes an item from staff assignment and decrements the count
    @classmethod
    def remove_item(cls, item_type, title):
        if item_type in staff_assignment and title in staff_assignment[item_type]:
            del staff_assignment[item_type][title]
            cls.decrement_item_count(item_type)
        else:
            print("Item not found.")

    # Searches for an item in the staff assignment by type and title
    @classmethod
    def search_item(cls, item_type, title):
        if item_type in staff_assignment:
            return staff_assignment[item_type].get(title, "Item not found.")
        return "Invalid item type."

    # Retrieves all items currently available in the library
    @classmethod
    def get_all_items(cls):
        return staff_assignment

# Class representing a Book, inherits from LibraryItem
class Book(LibraryItem):
    def __init__(self, title, author, genre, ISBN, pages, publication_year, language, shelf_location, condition):
        super().__init__(title, "Book", publication_year, language, shelf_location, condition)
        self._author = author  # Author of the book
        self._genre = genre  # Genre of the book
        self.ISBN = ISBN  # ISBN identifier
        self.pages = pages  # Number of pages

    # Method to check out a book
    def check_out(self):
        if self.available:
            self.available = False  # Mark as unavailable
            LibraryItem.decrement_item_count(self._item_type, self._title)  # Pass both item type and title
            print(f"Item '{self._title}' checked out successfully.")
        else:
            print(f"Item '{self._title}' is already unavailable.")

    # Method to return a book
    def return_item(self):
        if not self.available:
            self.available = True  # Mark as available again
            LibraryItem.increment_item_count(self._item_type, self._title)  # Pass both item type and title
            print(f"Item '{self._title}' returned successfully.")
        else:
            print(f"Item '{self._title}' is already available.")

    # String representation of the book
    def __str__(self):
        return (f"Book Title: {self._title}\nAuthor: {self._author}\nGenre: {self._genre}\n"
                f"ISBN: {self.ISBN}\nPages: {self.pages}\nPublication Year: {self.publication_year}\n"
                f"Language: {self.language}\nShelf Location: {self.shelf_location}\nCondition: {self.condition}")

class DVD(LibraryItem):
    def __init__(self, title, director, genre, duration, publication_year, language, shelf_location, condition):
        super().__init__(title, "DVD", publication_year, language, shelf_location, condition)
        self._director = director
        self._genre = genre
        self.duration = duration

    def check_out(self):
        print(f"\nAttempting to check out DVD '{self._title}'.")
        if self.available:
            self.available = False  # Mark as unavailable
            LibraryItem.decrement_item_count(self._item_type, self._title)  # Pass both item type and title
            print(f"Item '{self._title}' checked out successfully.")
        else:
            print(f"Item '{self._title}' is already unavailable.")

    def return_item(self):
        if not self.available:
            self.available = True  # Mark as available again
            LibraryItem.increment_item_count(self._item_type, self._title)  # Pass both item type and title
            print(f"Item '{self._title}' returned successfully.")
        else:
            print(f"Item '{self._title}' is already available.")

    def __str__(self):
        return (f"DVD Title: {self._title}\nDirector: {self._director}\nGenre: {self._genre}\n"
                f"Duration: {self.duration}\nPublication Year: {self.publication_year}\n"
                f"Language: {self.language}\nShelf Location: {self.shelf_location}\nCondition: {self.condition}")

class Magazine(LibraryItem):
    def __init__(self, title, issue, issue_number, publication_year, language, shelf_location, condition):
        super().__init__(title, "Magazine", publication_year, language, shelf_location, condition)
        self._issue = issue
        self.issue_number = issue_number

    def check_out(self):
        print(f"\nAttempting to check out Magazine '{self._title}'.")
        if self.available:
            self.available = False  # Mark as unavailable
            LibraryItem.decrement_item_count(self._item_type, self._title)  # Pass both item type and title
            print(f"Item '{self._title}' checked out successfully.")
        else:
            print(f"Item '{self._title}' is already unavailable.")

    def return_item(self):
        if not self.available:
            self.available = True  # Mark as available again
            LibraryItem.increment_item_count(self._item_type, self._title)  # Pass both item type and title
            print(f"Item '{self._title}' returned successfully.")
        else:
            print(f"Item '{self._title}' is already available.")

    def __str__(self):
        return (f"Magazine Title: {self._title}\nIssue: {self._issue}\nIssue Number: {self.issue_number}\n"
                f"Publication Year: {self.publication_year}\nLanguage: {self.language}\nShelf Location: {self.shelf_location}\nCondition: {self.condition}")
