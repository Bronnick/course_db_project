# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from tkinter import *
from tkinter import ttk

import psycopg2

from classes.Person import *
from database_module import SQLDatabase, GraphDB, AppDatabase
from ui.AppWindow import AppWindow

clicks = 0

# class AuthenticationWindow(Tk):
#     def __init__(self):
#         super().__init__()
#
#         # конфигурация окна
#         self.title("Новое окно")
#         self.geometry("250x200")
#
#         # определение кнопки
#         self.button = ttk.Button(self, text="закрыть")
#         self.button["command"] = self.button_clicked
#         self.button.pack(anchor="center", expand=1)
#
#     def button_clicked(self):
#         self.destroy()


def dismiss(window):
    window.grab_release()
    window.destroy()


def click():
    window = Toplevel()
    window.title("Новое окно")
    window.geometry("250x200")
    window.protocol("WM_DELETE_WINDOW", lambda: dismiss(window))  # перехватываем нажатие на крестик
    close_button = ttk.Button(window, text="Закрыть окно", command=lambda: dismiss(window))
    close_button.pack(anchor="center", expand=1)
    window.grab_set()


start_window = AppWindow()
start_window.mainloop()

person = Employee(1, input("input login"), 1234, 'John', 5000)

# sql_database.add_employee(person)


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
