import os
import tempfile
import uuid
from enum import Enum
from student import Student
from birthdate import Birthdate
import csv

class DatabaseInitState(Enum):
    DATABASE_CREATED = 0
    DATABASE_LOADED = 1

class Database:
    def __init__(self, filename):
        self.__filename = tempfile.gettempdir() + Database.__normalize_file_name(filename)
        self.__init_state = self.__create_file()
        self.__students = []

    # Accessors

    def get_file(self) -> str:
        return self.__filename

    def get_init_state(self) -> DatabaseInitState:
        return self.__init_state

    # Private methods

    @staticmethod
    def __normalize_file_name(filename: str) -> str:
        # Add a leading slash if not present
        if not filename.startswith(os.sep):
            return os.sep + filename

        return filename

    def __create_file(self) -> DatabaseInitState:
        try:
            open(self.get_file(), 'x')
            self.__write_header_row()
            return DatabaseInitState.DATABASE_CREATED
        except FileExistsError:
            return DatabaseInitState.DATABASE_LOADED

    def __write_header_row(self):
        print('Writing header row to file...')
        with open(self.get_file(), 'w') as csvfile:
            student_writer = csv.writer(csvfile)
            student_writer.writerow(['ID', 'Firstname', 'Lastname', 'Birthyear', 'Birthmonth', 'Birthday'])

    def __read_data(self) -> list[Student]:
        students = []

        with open(self.get_file()) as csvfile:
            student_reader = csv.reader(csvfile)
            for idx, row in enumerate(student_reader):
                birth_year = int(row[3])
                birth_month = int(row[4])
                birth_day = int(row[5])

                birthdate = Birthdate(birth_year, birth_month, birth_day)

                students.append(Student(row[1], row[2], birthdate, row[0]))

            return students


    def __save_data(self):
        with open(self.get_file(), 'w') as csvfile:
            student_writer = csv.writer(csvfile)
            for student in self.__students:
                student_writer.writerow(student.to_array())

    # Public methods

    def get_student(self, student_id: str|uuid.UUID) -> Student|None:
        self.__students = self.__read_data()

        if type(student_id) is uuid.UUID:
            student_id = str(student_id)

        student = next(filter(lambda stud: stud.get_id() == student_id, self.__students), None)

        return student

    def create_student(self, student: Student) -> Student:
        self.__students = self.__read_data()
        self.__students.append(student)
        self.__save_data()

        return student

    def update_student(self, student: Student) -> Student:
        self.__students = self.__read_data()

        student_to_update = next(filter(lambda stud: stud.get_id() == student.get_id(), self.__students), None)
        update_at = self.__students.index(student_to_update)

        self.__students[update_at] = student
        self.__save_data()

        return student

    def delete_student(self, student: Student) -> None:
        self.__students = self.__read_data()

        student_to_delete = next(filter(lambda stud: stud.get_id() == student.get_id(), self.__students), None)
        delete_at = self.__students.index(student_to_delete)

        del self.__students[delete_at]
        self.__save_data()