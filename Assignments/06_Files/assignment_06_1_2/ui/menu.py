from ui.list_students import ListStudents
from ui.add_student import AddStudent
from ui.update_student import UpdateStudent
from ui.delete_student import DeleteStudent
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
        print('1. List students')
        print('2. Add new student')
        print('3. Update a student')
        print('4. Delete a student')
        print('5. Exit')

        awaiting_valid_input = True

        error_msg = 'Please enter a valid number! (1 - 5)'

        while awaiting_valid_input:
            try:
                self.__selected_option = int(input('Enter your choice: '))

                if 1 <= self.__selected_option <= 5:
                    awaiting_valid_input = False
                else:
                    print(error_msg)
            except ValueError:
                print(error_msg)

        if self.__selected_option == 1:
            ListStudents(self.__database).execute()
        elif self.__selected_option == 2:
            AddStudent(self.__database).execute()
        elif self.__selected_option == 3:
            UpdateStudent(self.__database).execute()
        elif self.__selected_option == 4:
            DeleteStudent(self.__database).execute()
        else:
            exit()