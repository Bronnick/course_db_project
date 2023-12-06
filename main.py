# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from tkinter import *
from tkinter import ttk

import psycopg2

from classes.Person import *
from database_module import SQLDatabase, GraphDB, AppDatabase
from datetime import datetime

from ui.AppWindow import AppWindow

# print((datetime.strptime('2022.02.12', '%Y.%m.%d') - datetime.strptime('2020.03.23', '%Y.%m.%d')))
AppWindow().mainloop()

# sql_database.add_employee(person)


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
