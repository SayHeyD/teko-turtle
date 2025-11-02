from time import sleep
import os
import shutil

from database import Database
from ui import menu

class CsvExport:

    def __init__(self, database: Database):
        self.__database = database
        self.__filepath = None

    def __file_exists(self) -> bool:
        try:
            with open(self.__filepath, 'r') as file:
                return True
        except FileNotFoundError:
            return False

    def __create_directories_of_path(self):
        dir_path = os.sep.join(self.__filepath.split(os.sep)[:-1])

        if not os.path.isdir(dir_path):
            os.makedirs(dir_path, exist_ok=True)

    def __export(self) -> None:
        self.__filepath = input('Enter file path: ')

        if self.__file_exists():
            print('File already exists!')
            print('Please enter a path to a file that does not exist yet!')
            print('Returning to main menu...')
            sleep(3)
            menu.Menu(self.__database).draw()

        self.__create_directories_of_path()

        shutil.copy(self.__database.get_file(), self.__filepath)

        print('File exported!')
        sleep(3)

    def execute(self):
        self.__export()
        menu.Menu(self.__database).draw()