from datetime import datetime
from database import Database
from student import Student
from birthdate import Birthdate
from ui import menu

class AddStudent:

    def __init__(self, database: Database):
        self.__database = database
        self.__firstname = None
        self.__lastname = None
        self.__birth_year = None
        self.__birth_month = None
        self.__birth_day = None

    def __steps(self):
        return [
            self.__get_firstname,
            self.__get_lastname,
            self.__get_birth_year,
            self.__get_birth_month,
            self.__get_birth_day,
        ]

    def __get_firstname(self) -> None:
        self.__firstname = input('Vorname: ')

    def __get_lastname(self) -> None:
        self.__lastname = input('Nachname: ')

    def __get_birth_year(self) -> None:
        year = None

        awaiting_valid_input = True

        while awaiting_valid_input:
            year = input('Geburtsjahr: ')

            current_year = datetime.now().year

            if year.isnumeric() and 1900 <= int(year) <= current_year:
                awaiting_valid_input = False
            else:
                print(f'Birthyear must be a valid year! (1900 - {current_year})')

        self.__birth_year = int(year)

    def __get_birth_month(self) -> None:
        month = None

        awaiting_valid_input = True

        while awaiting_valid_input:
            month = input('Monat: ')

            if month.isnumeric() and 1 <= int(month) <= 12:
                awaiting_valid_input = False
            else:
                print('Month must be a valid month! (1 - 12)')

        self.__birth_month = int(month)

    def __get_birth_day(self) -> None:
        day = None

        awaiting_valid_input = True

        while awaiting_valid_input:
            day = input('Tag: ')

            if day.isnumeric() and 1 <= int(day) <= 31:
                awaiting_valid_input = False
            else:
                print('Month must be a valid month! (1 - 12)')

        self.__birth_day = int(day)

    def __create(self) -> Student:
        birthdate = Birthdate(self.__birth_year, self.__birth_month, self.__birth_day)
        student = Student(self.__firstname, self.__lastname, birthdate)

        return self.__database.create_student(student)

    def execute(self):
        for step in self.__steps():
            step()

        self.__create()
        menu.Menu(self.__database).draw()
