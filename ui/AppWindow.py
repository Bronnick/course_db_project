from tkinter import Toplevel, ttk, IntVar
from tkinter.constants import SE, BOTH, END
from tkinter.tix import Tk

from classes.Person import Person, Employee, Admin, Manager
from database_module import AppDatabase

app_db = AppDatabase()

LOGIN_ENTRY_WIDGET = 'login_entry'
PASSWORD_ENTRY_WIDGET = 'password_entry'
ADMIN_CHECK_WIDGET = 'admin_check'
AUTH_RESULT_WIDGET = 'auth_result'

LOGIN_ENTRY_EMPLOYEE_ADD_WIDGET = 'login_employee_add'
PASSWORD_ENTRY_EMPLOYEE_ADD_WIDGET = 'password_employee_add'
NAME_ENTRY_EMPLOYEE_ADD_WIDGET = 'name_employee_add'
SALARY_ENTRY_EMPLOYEE_ADD_WIDGET = 'salary_employee_add'
DEPARTMENT_ENTRY_EMPLOYEE_ADD_WIDGET = 'department_employee_add'
ROLE_ENTRY_EMPLOYEE_ADD_WIDGET = 'role_employee_add'


class AppWindow(Tk):
    def __init__(self):
        super().__init__()
        self.title("Authentication")
        self.geometry("500x500")

        self.widgets = {}
        self.admin_var = IntVar()
        self.create_auth_window()

    def create_auth_window(self):
        self.clear_widgets()
        login_label = ttk.Label(self, text="Login: ")
        login_label.place(x=175, y=200)
        login_entry = ttk.Entry(self)
        login_entry.place(x=250, y=200)
        self.widgets[LOGIN_ENTRY_WIDGET] = login_entry

        password_label = ttk.Label(self, text="Password: ")
        password_label.place(x=175, y=250)
        password_entry = ttk.Entry(self)
        password_entry.place(x=250, y=250)
        self.widgets[PASSWORD_ENTRY_WIDGET] = password_entry

        admin_checkbutton = ttk.Checkbutton(self, text="I am admin", variable=self.admin_var)
        admin_checkbutton.place(x=230, y=300)
        self.widgets[ADMIN_CHECK_WIDGET] = admin_checkbutton

        auth_button = ttk.Button(self, text="Log in", command=self.auth_button_click)
        auth_button.place(x=210, y=350)

        auth_result_label = ttk.Label(self, text="")
        auth_result_label.place(x=200, y=400)
        self.widgets[AUTH_RESULT_WIDGET] = auth_result_label

        close_button = ttk.Button(self, text="Exit", command=self.destroy)
        close_button.place(x=400, y=450)

    def create_user_data_window(self, person):
        # self.title("Новое окно")
        # self.geometry("250x200")
        # # self.protocol("WM_DELETE_WINDOW", lambda: self.dismiss())
        self.clear_widgets()

        id_label = ttk.Label(text="Id: ")
        id_label.place(x=25, y=25)
        _id = ttk.Label(text=person.id)
        _id.place(x=100, y=25)

        login_label = ttk.Label(text="Login: ")
        login_label.place(x=25, y=50)
        login = ttk.Label(text=person.login)
        login.place(x=100, y=50)

        password_label = ttk.Label(text="Password: ")
        password_label.place(x=25, y=75)
        password = ttk.Label(text='*' * len(person.password))
        password.place(x=100, y=75)

        name_label = ttk.Label(text="Name: ")
        name_label.place(x=25, y=100)
        name = ttk.Label(text=person.name)
        name.place(x=100, y=100)

        name_label = ttk.Label(text="Salary: ")
        name_label.place(x=25, y=125)
        name = ttk.Label(text=person.salary)
        name.place(x=100, y=125)

        department_label = ttk.Label(text="Department: ")
        department_label.place(x=25, y=150)
        department = ttk.Label(text=person.department)
        department.place(x=100, y=150)

        role_label = ttk.Label(text="Role: ")
        role_label.place(x=25, y=175)
        if isinstance(person, Manager):
            role_text = 'manager'
        else:
            role_text = 'employee'
        role = ttk.Label(text=role_text)
        role.place(x=100, y=175)

        button_log_out = ttk.Button(text="Log out", command=self.create_auth_window)
        button_log_out.place(relx=0.8, rely=0.8)

    def create_manager_window(self, person):
        self.create_user_data_window(person)

        button_view_employees = ttk.Button(text="View employees", command=self.view_salary_increase_requests)
        button_view_employees.place(x=75, y=200)

    def create_admin_window(self, admin):
        self.clear_widgets()

        access_level_label = ttk.Label(self, text="Access level: ")
        access_level_label.place(x=25, y=25)
        access_level = ttk.Label(self, text=admin.access_level)
        access_level.place(x=100, y=25)

        add_employee_button = ttk.Button(self, text="Add employee",
                                         command=lambda: self.create_employee_add_window(admin))
        add_employee_button.place(x=25, y=75)

        back_button = ttk.Button(self, text="Back", command=self.create_auth_window)
        back_button.place(relx=0.8, rely=0.8)

    def create_employee_add_window(self, admin):
        self.clear_widgets()

        login_label = ttk.Label(text="Login: ")
        login_label.place(x=25, y=50)
        login_entry = ttk.Entry(self)
        login_entry.place(x=100, y=50)
        self.widgets[LOGIN_ENTRY_EMPLOYEE_ADD_WIDGET] = login_entry

        password_label = ttk.Label(text="Password: ")
        password_label.place(x=25, y=75)
        password_entry = ttk.Entry(self)
        password_entry.place(x=100, y=75)
        self.widgets[PASSWORD_ENTRY_EMPLOYEE_ADD_WIDGET] = password_entry

        name_label = ttk.Label(text="Name: ")
        name_label.place(x=25, y=100)
        name_entry = ttk.Entry(self)
        name_entry.place(x=100, y=100)
        self.widgets[NAME_ENTRY_EMPLOYEE_ADD_WIDGET] = name_entry

        salary_label = ttk.Label(text="Salary: ")
        salary_label.place(x=25, y=125)
        salary_entry = ttk.Entry(self)
        salary_entry.place(x=100, y=125)
        self.widgets[SALARY_ENTRY_EMPLOYEE_ADD_WIDGET] = salary_entry

        department_label = ttk.Label(text="Salary: ")
        department_label.place(x=25, y=150)
        department_entry = ttk.Entry(self)
        department_entry.place(x=100, y=150)
        self.widgets[DEPARTMENT_ENTRY_EMPLOYEE_ADD_WIDGET] = department_entry

        role_label = ttk.Label(text="Role: ")
        role_label.place(x=25, y=175)
        role_entry = ttk.Entry(self)
        role_entry.place(x=100, y=175)
        self.widgets[ROLE_ENTRY_EMPLOYEE_ADD_WIDGET] = role_entry

        button_add_employee = ttk.Button(self, text='Add employee',
                                         command=lambda: self.add_employee_button_click(admin))
        button_add_employee.place(x=100, y=200)

        back_button = ttk.Button(self, text="Back", command=lambda: self.create_admin_window(admin))
        back_button.place(relx=0.8, rely=0.8)

    # def create_view_employee_window(self):
    #     self.clear_widgets()
    #
    #     people = []
    #
    #     people_data = app_db.get_all_employees()
    #     for item in people_data:
    #         print(item[0][1])
    #         print(item[1][0])
    #         people.append((item[0][0], item[0][1], item[0][2], item[1][0], '', ''))
    #
    #     for item in people:
    #         print(item)
    #
    #     columns = ("id", "name", "salary")
    #     table = ttk.Treeview(columns=columns, show="headings")
    #     table.pack(fill=BOTH, expand=1)
    #
    #     table.heading("id", text="id")
    #     table.heading("name", text='name')
    #     table.heading("salary", text='salary')
    #
    #     for person in people:
    #         table.insert("", END, values=person)

    def view_salary_increase_requests(self):
        pass

    def auth_button_click(self):
        if self.admin_var.get() == 0:
            auth_result = app_db.authenticate_employee(self.widgets[LOGIN_ENTRY_WIDGET].get(),
                                                       self.widgets[PASSWORD_ENTRY_WIDGET].get(),
                                                       self.admin_var.get())
            if auth_result != -1:
                self.widgets[AUTH_RESULT_WIDGET]['text'] = "Authentication succeeded"
            else:
                self.widgets[AUTH_RESULT_WIDGET]['text'] = 'Authentication failed'
                return
            if auth_result[0][0][3] == 'employee':
                person = Employee(auth_result[0][0][0], self.widgets[LOGIN_ENTRY_WIDGET].get(),
                                  self.widgets[PASSWORD_ENTRY_WIDGET].get(), auth_result[0][0][1], auth_result[0][0][2],
                                  auth_result[1])
                self.create_user_data_window(person)
            else:
                person = Manager(auth_result[0][0][0], self.widgets[LOGIN_ENTRY_WIDGET].get(),
                                 self.widgets[PASSWORD_ENTRY_WIDGET].get(), auth_result[0][0][1], auth_result[0][0][2],
                                 auth_result[1])
                self.create_manager_window(person)
        else:
            auth_result = app_db.authenticate_employee(self.widgets[LOGIN_ENTRY_WIDGET].get(),
                                                       self.widgets[PASSWORD_ENTRY_WIDGET].get(),
                                                       self.admin_var.get())
            if auth_result != -1:
                self.widgets[AUTH_RESULT_WIDGET]['text'] = "Authentication succeeded"
            else:
                self.widgets[AUTH_RESULT_WIDGET]['text'] = 'Authentication failed'
                return
            admin = Admin(auth_result[0][0], auth_result[0][1], auth_result[0][2], '', auth_result[0][3])
            self.create_admin_window(admin)

    def add_employee_button_click(self, admin):
        employee = None
        if self.widgets[ROLE_ENTRY_EMPLOYEE_ADD_WIDGET].get() == 'employee':
            employee = Employee(0, self.widgets[LOGIN_ENTRY_EMPLOYEE_ADD_WIDGET].get(),
                                self.widgets[PASSWORD_ENTRY_EMPLOYEE_ADD_WIDGET].get(),
                                self.widgets[NAME_ENTRY_EMPLOYEE_ADD_WIDGET].get(),
                                self.widgets[SALARY_ENTRY_EMPLOYEE_ADD_WIDGET].get(),
                                self.widgets[DEPARTMENT_ENTRY_EMPLOYEE_ADD_WIDGET].get())
        else:
            employee = Manager(0, self.widgets[LOGIN_ENTRY_EMPLOYEE_ADD_WIDGET].get(),
                               self.widgets[PASSWORD_ENTRY_EMPLOYEE_ADD_WIDGET].get(),
                               self.widgets[NAME_ENTRY_EMPLOYEE_ADD_WIDGET].get(),
                               self.widgets[SALARY_ENTRY_EMPLOYEE_ADD_WIDGET].get(),
                               self.widgets[DEPARTMENT_ENTRY_EMPLOYEE_ADD_WIDGET].get())
        app_db.add_employee(employee)
        self.create_admin_window(admin)

    def clear_widgets(self):
        widget_list = self.all_children()
        for item in widget_list:
            item.place_forget()

    def all_children(self):
        _list = self.winfo_children()

        for item in _list:
            if item.winfo_children():
                _list.extend(item.winfo_children())

        return _list


class UserDataWindow(Tk):
    def __init__(self, person):
        super().__init__()
        self.title("Новое окно")
        self.geometry("250x200")
        # self.protocol("WM_DELETE_WINDOW", lambda: self.dismiss())

        self.id_label = ttk.Label(text="Id: ")
        self.id_label.place(x=25, y=25)
        self.id = ttk.Label(text=person.id)
        self.id.place(x=100, y=25)

        self.login_label = ttk.Label(text="Login: ")
        self.login_label.place(x=25, y=50)
        self.login = ttk.Label(text=person.login)
        self.login.place(x=100, y=50)

        self.password_label = ttk.Label(text="Password: ")
        self.password_label.place(x=25, y=75)
        self.password = ttk.Label(text='*' * len(person.password))
        self.password.place(x=100, y=75)

        self.name_label = ttk.Label(text="Name: ")
        self.name_label.place(x=25, y=100)
        self.name = ttk.Label(text=person.name)
        self.name.place(x=100, y=100)

        self.name_label = ttk.Label(text="Salary: ")
        self.name_label.place(x=25, y=125)
        self.name = ttk.Label(text=person.salary)
        self.name.place(x=100, y=125)

        self.button_log_out = ttk.Button(text="Log out", command=self.go_to_auth_window)
        self.button_log_out.place(relx=0.8, rely=0.8)

        # columns = ("worker_id", "login", "password", "name", "salary")
        # self.table = ttk.Treeview(columns=columns, show="headings")
        # self.table.pack(fill=BOTH, expand=1)
        #
        # self.table.heading("worker_id", text='id')
        # self.table.heading("login", text='login')
        # self.table.heading("password", text='password')
        # self.table.heading("name", text='name')
        # self.table.heading("salary", text='salary')
        #
        # self.table.insert("", END, values=person)
        # self.mainloop()
        self.destroy()

    def clear_widgets(self):
        widget_list = self.all_children()
        for item in widget_list:
            item.place_forget()

    def all_children(self):
        _list = self.winfo_children()

        for item in _list:
            if item.winfo_children():
                _list.extend(item.winfo_children())

        return _list
