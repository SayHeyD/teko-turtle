from database import Database
from student import Student
from ui import menu

class MonthWithMostBirthdays:

    def __init__(self, database: Database):
        self.__database = database
        self.__students = []

    def __get_month_counts(self) -> dict[int, int]:
        self.__students = self.__database.get_students()
        month_counts = {}

        for student in self.__students:
            month = student.get_age().get_month()
            month_counts[month] = month_counts.get(month, 0) + 1

        return month_counts

    def __month_with_most_birthdays(self):
        month_counts = self.__get_month_counts()

        return max(month_counts, key=month_counts.get)


    def execute(self) -> None:

        print('Month with most birthdays:')
        print(self.__month_with_most_birthdays())

        print('Press enter to return to main menu...')
        input()
        menu.Menu(self.__database).draw()
