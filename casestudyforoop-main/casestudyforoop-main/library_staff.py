class LibraryStaff:
    _staff_count = 0

    def __init__(self, staff_station):
        self.staff_station = staff_station
        LibraryStaff._staff_count += 1

    def check_out_item(self, patron, item):
        patron.borrow_item(item)

    def check_in_item(self, patron, item):
        patron.return_item(item)

    @staticmethod
    def total_staff():
        return LibraryStaff._staff_count
    