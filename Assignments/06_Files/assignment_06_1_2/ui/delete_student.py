from time import sleep

from database import Database
from student import Student
from birthdate import Birthdate
from ui import menu

class DeleteStudent:

    def __init__(self, database: Database):
        self.__database = database

    def __delete(self) -> None:

        student_id = input('Enter student ID: ')
        student = self.__database.get_student(student_id)

        if student is None:
            print('No student found with that ID!')
            print('Returning to main menu...')
            return

        self.__database.delete_student(student)
        print('Student deleted!')
        sleep(3)

    def execute(self):
        self.__delete()
        menu.Menu(self.__database).draw()
