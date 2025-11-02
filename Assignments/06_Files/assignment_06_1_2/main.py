import uuid
from database import Database
from student import Student
from birthdate import Birthdate

def main_menu():
    while True:
        print('=======================================')
        print('‖         Student Database 👨🏼‍🎓         ‖')
        print('=======================================')
        print()
        print()
        print('1. Add new student')
        print('2. Search for student')
        print('3. Exit')

file_name = 'assignment_06_1_2.csv'

db = Database(file_name)

student = db.get_student('6d0a0127-2512-41f7-a080-da656be32353')
db.delete_student(student)

print(db.get_file())