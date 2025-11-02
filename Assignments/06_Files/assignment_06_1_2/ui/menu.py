from ui.add_student import AddStudent
from ui.list_students import ListStudents
from database import Database

class Menu:

    def __init__(self, database: Database):
        self.__database = database
        self.__selected_option = 0

    def draw(self) -> None:
        print('======================================')
        print('‖         Student Database 👨🏼‍🎓         ‖')
        print('======================================')
        print()
        print('What would you like to do?')
        print()
        print('1. Add new student')
        print('2. List students')
        print('3. Exit')

        awaiting_valid_input = True

        error_msg = 'Please enter a valid number! (1 - 3)'

        while awaiting_valid_input:
            try:
                self.__selected_option = int(input('Enter your choice: '))

                if 1 <= self.__selected_option <= 3:
                    awaiting_valid_input = False
                else:
                    print(error_msg)
            except ValueError:
                print(error_msg)

        if self.__selected_option == 1:
            AddStudent(self.__database).execute()
        elif self.__selected_option == 2:
            ListStudents(self.__database).execute()
        else:
            exit()