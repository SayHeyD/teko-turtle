from ui import menu
from database import Database

file_name = 'assignment_06_1_2.csv'

db = Database(file_name)

print(db.get_file())

menu.Menu(db).draw()