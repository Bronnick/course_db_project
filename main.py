# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from tkinter import *
from tkinter import ttk

import psycopg2

from classes.Person import *
from database_module import SQLDatabase, GraphDB, AppDatabase
from ui.AppWindow import AppWindow

AppWindow().mainloop()

# sql_database.add_employee(person)


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
