from ui import menu
from database import Database


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

print(db.get_file())

menu.Menu(db).draw()