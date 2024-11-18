import json

def load_staff_assignment_from_file(filename):
    with open(filename, 'r') as file:
        return json.load(file)

staff_assignment = load_staff_assignment_from_file('staff_assignment.txt')