from database import Database
from ui import menu
from ui.table import Table

class ListStudents:

    def __init__(self, database: Database):
        self.__database = database
        self.__students = []

    def __print_table(self) -> None:
        headers = ['ID', 'Firstname', 'Lastname', 'Birthyear', 'Birthmonth', 'Birthday']
        rows = [s.to_array() for s in self.__students]
        Table(headers, rows).print_table()

    def __sort_students(self) -> None:

        descending = True

        while True:
            sorting_attribute = input('Sort by: Firstname [0], Lastname [1], Age [2]: ')
            if sorting_attribute in ['0', '1', '2', '3']:
                break
            else:
                print('Invalid sorting attribute!')

        while True:
            sort_direction = input('Sort direction: Ascending [1], Descending [2]: ')
            if sort_direction in ['1', '2']:
                break
            else:
                print('Invalid sorting direction!')

        if sort_direction == '2':
            descending = False

        if sorting_attribute == '0':
            self.__students.sort(key=lambda student: student.get_firstname(), reverse=descending)
        elif sorting_attribute == '1':
            self.__students.sort(key=lambda student: student.get_lastname(), reverse=descending)
        elif sorting_attribute == '2':
            self.__students.sort(key=lambda student: student.get_age().to_date(), reverse=descending)

        self.__print_table()

    def execute(self) -> None:
        self.__students = self.__database.get_students()

        self.__print_table()

        while True:
            print('Actions: [Enter] - Return to main menu. | [s] - Sort students')
            action = input()

            if action == 's':
                self.__sort_students()
            elif action == '':
                menu.Menu(self.__database).draw()
            else:
                print('Invalid action!')
