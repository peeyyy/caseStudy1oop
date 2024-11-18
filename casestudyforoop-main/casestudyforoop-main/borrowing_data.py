def append_borrowing_data(patron_name, item_title, date_borrowed, due_date, item_type):
    filename = f'borrowing_data_{item_type.lower()}.txt'
    with open(filename, 'a') as file:
        file.write(f"Patron Name: {patron_name}, Item Title: {item_title}, Date Borrowed: {date_borrowed}, Due Date: {due_date}\n")
    
    # Automatically sort after adding a new entry
    sort_borrowing_data(item_type)


def delete_borrowing_data(patron_name, item_title, item_type):
    filename = f'borrowing_data_{item_type.lower()}.txt'
    with open(filename, 'r') as file:
        lines = file.readlines()

    with open(filename, 'w') as file:
        for line in lines:
            if not (f"Patron Name: {patron_name}, Item Title: {item_title}" in line):
                file.write(line)

    # Automatically sort after deleting an entry
    sort_borrowing_data(item_type)

def return_append_return_data(patron_name, item_title, date_borrowed, due_date, date_return, return_type, item_type):
    filename = f'return_data_{item_type.lower()}.txt'
    with open(filename, 'a') as file:
        file.write(f"Patron Name: {patron_name}, Item Title: {item_title}, Date Borrowed: {date_borrowed}, Due Date: {due_date}, Date Returned: {date_return}, Return: {return_type}\n")
    
    # Automatically sort after adding a new entry
    sort_borrowing_data(item_type)


def sort_borrowing_data(item_type):
    filename = f'borrowing_data_{item_type.lower()}.txt'
    
    # Step 1: Read and load each line from the file
    with open(filename, 'r') as file:
        lines = file.readlines()

    # Step 2: Sort lines alphabetically by patron name
    lines.sort(key=lambda line: line.split(",")[0].split(": ")[1].strip())

    # Step 3: Write the sorted lines back to the file
    with open(filename, 'w') as file:
        file.writelines(lines)