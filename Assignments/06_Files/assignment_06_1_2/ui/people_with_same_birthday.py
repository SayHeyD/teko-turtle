from database import Database
from student import Student
from ui import menu
from ui.table import Table

class PeopleWithSameBirthday:

    def __init__(self, database: Database):
        self.__database = database
        self.__students = []

    def __find_students_with_same_birthday(self) -> list[Student]:
        all_students = self.__database.get_students()
        by_month_day: dict[tuple[int, int], list[Student]] = {}
        for s in all_students:
            key = (s.get_age().get_month(), s.get_age().get_day())
            by_month_day.setdefault(key, []).append(s)
        duplicates: list[Student] = []
        for group in by_month_day.values():
            if len(group) >= 2:
                duplicates.extend(group)
        return duplicates

    def __print_table(self) -> None:
        headers = ['ID', 'Firstname', 'Lastname', 'Birthyear', 'Birthmonth', 'Birthday']
        rows = [s.to_array() for s in self.__students]
        Table(headers, rows).print_table()

    def execute(self) -> None:
        # Find students that share the same birthday (same month and day, any year)
        self.__students = self.__find_students_with_same_birthday()

        if len(self.__students) == 0:
            print('No students share the same birthday.')
            print('Press enter to return to main menu...')
            input()
            menu.Menu(self.__database).draw()
            return

        print('Students with the same birthday:')
        self.__print_table()

        print('Press enter to return to main menu...')
        input()
        menu.Menu(self.__database).draw()
