from datetime import datetime
from time import sleep

from database import Database
from student import Student
from birthdate import Birthdate
from ui import menu

class UpdateStudent:

    def __init__(self, database: Database):
        self.__database = database
        self.__firstname = None
        self.__lastname = None
        self.__birth_year = None
        self.__birth_month = None
        self.__birth_day = None

        self.__student = None

    def __steps(self):
        return [
            self.__get_firstname,
            self.__get_lastname,
            self.__get_birth_year,
            self.__get_birth_month,
            self.__get_birth_day,
        ]

    def __get_firstname(self) -> None:
        firstname = input(f'Vorname [{self.__student.get_firstname()}]: ')

        if firstname == '':
            firstname = self.__student.get_firstname()

        self.__firstname = firstname

    def __get_lastname(self) -> None:
        lastname = input(f'Nachname [{self.__student.get_lastname()}]: ')

        if lastname == '':
            lastname = self.__student.get_lastname()

        self.__lastname = lastname

    def __get_birth_year(self) -> None:
        year = None

        awaiting_valid_input = True

        while awaiting_valid_input:
            year = input(f'Geburtsjahr [{self.__student.get_age().get_year()}]: ')

            if year == '':
                year = str(self.__student.get_age().get_year())

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
            month = input(f'Monat [{self.__student.get_age().get_month()}]: ')

            if month == '':
                month = str(self.__student.get_age().get_month())

            if month.isnumeric() and 1 <= int(month) <= 12:
                awaiting_valid_input = False
            else:
                print('Month must be a valid month! (1 - 12)')

        self.__birth_month = int(month)

    def __get_birth_day(self) -> None:
        day = None

        awaiting_valid_input = True

        while awaiting_valid_input:
            day = input(f'Tag [{self.__student.get_age().get_day()}]: ')

            if day == '':
                day = str(self.__student.get_age().get_day())

            if day.isnumeric() and 1 <= int(day) <= 31:
                awaiting_valid_input = False
            else:
                print('Month must be a valid month! (1 - 12)')

        self.__birth_day = int(day)

    def __update(self) -> Student:
        birthdate = Birthdate(self.__birth_year, self.__birth_month, self.__birth_day)
        student = Student(self.__firstname, self.__lastname, birthdate, self.__student.get_id())

        return self.__database.update_student(student)

    def execute(self):
        student_id = input('Enter student ID: ')
        self.__student = self.__database.get_student(student_id)

        if self.__student is None:
            print('No student found with that ID!')
            print('Returning to main menu...')
            sleep(3)
            menu.Menu(self.__database).draw()

        for step in self.__steps():
            step()

        self.__update()
        menu.Menu(self.__database).draw()
