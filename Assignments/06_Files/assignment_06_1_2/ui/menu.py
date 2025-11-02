from ui.list_students import ListStudents
from ui.month_with_most_birthdays import MonthWithMostBirthdays
from ui.add_student import AddStudent
from ui.update_student import UpdateStudent
from ui.delete_student import DeleteStudent
from ui.csv_export import CsvExport
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
        print('2. Month with most birthdays')
        print('3. Add new student')
        print('4. Update a student')
        print('5. Delete a student')
        print('6. Export to CSV')
        print('7. Exit')

        awaiting_valid_input = True

        error_msg = 'Please enter a valid number! (1 - 6)'

        while awaiting_valid_input:
            try:
                self.__selected_option = int(input('Enter your choice: '))

                if 1 <= self.__selected_option <= 6:
                    awaiting_valid_input = False
                else:
                    print(error_msg)
            except ValueError:
                print(error_msg)

        if self.__selected_option == 1:
            ListStudents(self.__database).execute()
        elif self.__selected_option == 2:
            MonthWithMostBirthdays(self.__database).execute()
        elif self.__selected_option == 3:
            AddStudent(self.__database).execute()
        elif self.__selected_option == 4:
            UpdateStudent(self.__database).execute()
        elif self.__selected_option == 5:
            DeleteStudent(self.__database).execute()
        elif self.__selected_option == 6:
            CsvExport(self.__database).execute()
        else:
            exit()