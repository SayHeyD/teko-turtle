from database import Database
from student import Student
from ui import menu

class ListStudents:

    def __init__(self, database: Database):
        self.__database = database
        self.__students = []

    def __get_max_column_length(self, header: str, column_index: int) -> int:
        max_length = len(header) + 2

        for student in self.__students:

            if column_index == 0:
                value = student.get_id()
            elif column_index == 1:
                value = student.get_firstname()
            elif column_index == 2:
                value = student.get_lastname()
            elif column_index == 3:
                value = student.get_age().get_year()
            elif column_index == 4:
                value = student.get_age().get_month()
            elif column_index == 5:
                value = student.get_age().get_day()
            else:
                raise Exception('Invalid column index!')

            value_length = len(str(value)) + 2

            if value_length > max_length:
                max_length = value_length

        return max_length

    def __get_all_column_lengths(self) -> list[int]:
        return [
            self.__get_max_column_length('ID', 0),
            self.__get_max_column_length('Firstname', 1),
            self.__get_max_column_length('Lastname', 2),
            self.__get_max_column_length('Birthyear', 3),
            self.__get_max_column_length('Birthmonth', 4),
            self.__get_max_column_length('Birthday', 5),
        ]

    def __print_header_row(self) -> None:

        column_lengths = self.__get_all_column_lengths()

        self.__print_seperator_row()

        print('| ID'.ljust(column_lengths[0]), end=' ')
        print('| Firstname'.ljust(column_lengths[1]), end=' ')
        print('| Lastname'.ljust(column_lengths[2]), end=' ')
        print('| Birthyear'.ljust(column_lengths[3]), end=' ')
        print('| Birthmonth'.ljust(column_lengths[4]), end=' ')
        print('| Birthday'.ljust(column_lengths[5]) + ' |')

        self.__print_seperator_row()

    def __print_seperator(self, length: int) -> None:
        print('+'.ljust(length, '-'), end='-')

    def __print_seperator_row(self) -> None:
        column_lengths = self.__get_all_column_lengths()

        for column_length in column_lengths:
            self.__print_seperator(column_length)

        print('+')

    def __print_data_row(self, student: Student) -> None:
        column_lengths = self.__get_all_column_lengths()

        print(f'| {student.get_id()}'.ljust(column_lengths[0]), end=' ')
        print(f'| {student.get_firstname()}'.ljust(column_lengths[1]), end=' ')
        print(f'| {student.get_lastname()}'.ljust(column_lengths[2]), end=' ')
        print(f'| {student.get_age().get_year()}'.ljust(column_lengths[3]), end=' ')
        print(f'| {student.get_age().get_month()}'.ljust(column_lengths[4]), end=' ')
        print(f'| {student.get_age().get_day()}'.ljust(column_lengths[5]) + ' |')

    def __print_table(self, students: list[Student]) -> None:
        self.__print_header_row()

        for student in students:
            self.__print_data_row(student)

        self.__print_seperator_row()

    def execute(self) -> None:
        self.__students = self.__database.get_students()

        self.__print_table(self.__students)

        input('Press Enter to return to main menu')
        menu.Menu(self.__database).draw()
