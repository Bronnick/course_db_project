from datetime import datetime
from tkinter import Toplevel, ttk, IntVar
from tkinter.constants import SE, BOTH, END, NO
from tkinter.tix import Tk

from classes.Absence import SickLeave
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
BIRTH_YEAR_ENTRY_EMPLOYEE_ADD_WIDGET = 'birth_year_employee_add'
FAMILY_STATE_ENTRY_EMPLOYEE_ADD_WIDGET = 'family_state_employee_add'
GENDER_ENTRY_EMPLOYEE_ADD_WIDGET = 'gender_employee_add'
KIDS_AMOUNT_ENTRY_EMPLOYEE_ADD_WIDGET = 'kids_amount_employee_add'

START_ILLNESS_DATE_WIDGET = "start_illness_date"
DURATION_ILLNESS_WIDGET = "duration_illness"
ILLNESS_TYPE_WIDGET = "type_illness"
LOGIN_ENTRY_WIDGET_ILLNESS = "login_illness"

AVERAGE_SALARY_MALE_LABEL = "average_salary_men"
AVERAGE_SALARY_FEMALE_LABEL = "average_salary_women"


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

        birth_year_label = ttk.Label(text="Birth year: ")
        birth_year_label.place(x=25, y=200)
        birth_year_entry = ttk.Label(text=person.birth_year)
        birth_year_entry.place(x=100, y=200)

        family_state_label = ttk.Label(text="Family state: ")
        family_state_label.place(x=25, y=225)
        family_state_entry = ttk.Label(text=person.family_state)
        family_state_entry.place(x=100, y=225)

        gender_label = ttk.Label(text="Gender: ")
        gender_label.place(x=25, y=250)
        gender_entry = ttk.Label(text=person.gender)
        gender_entry.place(x=100, y=250)

        kids_amount_label = ttk.Label(text="Kids amount: ")
        kids_amount_label.place(x=25, y=275)
        kids_amount_entry = ttk.Label(text=person.kids_amount)
        kids_amount_entry.place(x=100, y=275)

        start_date_label = ttk.Label(text="Start date: ")
        start_date_label.place(x=25, y=300)
        start_date_entry = ttk.Label(text=person.start_date)
        start_date_entry.place(x=100, y=300)

        button_view_sick_leaves = ttk.Button(text="View sick leaves",
                                             command=lambda: self.create_sick_leaves_window(person))
        button_view_sick_leaves.place(x=70, y=350)

        button_log_out = ttk.Button(text="Log out", command=self.create_auth_window)
        button_log_out.place(relx=0.8, rely=0.8)

    def create_manager_window(self, person):
        self.create_user_data_window(person)

        id_label = ttk.Label(text="Reports: ")
        id_label.place(x=300, y=25)

        button_view_pensioners = ttk.Button(text="View pensioners",
                                            command=lambda: self.create_pensioners_window(person))
        button_view_pensioners.place(x=300, y=50)

        button_view_salary_less_than = ttk.Button(text="View salaries less than N",
                                                  command=lambda: self.create_salary_less_than_window(100000, person))
        button_view_salary_less_than.place(x=300, y=75)

        button_view_average_age = ttk.Button(text="View average age",
                                             command=lambda: self.create_average_age_window(person.department, person))
        button_view_average_age.place(x=300, y=100)

        button_view_sick_leave_duration = ttk.Button(text="View sick leaves duration",
                                                     command=lambda: self.create_sick_leave_duration_window(person))
        button_view_sick_leave_duration.place(x=300, y=125)

        button_view_average_experience = ttk.Button(text="View average experience",
                                                    command=lambda: self.create_average_experience_window(person))
        button_view_average_experience.place(x=300, y=150)
        button_view_average_salary = ttk.Button(text="View average salary",
                                                command=lambda: self.create_average_salary_window(person))
        button_view_average_salary.place(x=300, y=175)

    def create_admin_window(self, admin):
        self.clear_widgets()

        access_level_label = ttk.Label(self, text="Access level: ")
        access_level_label.place(x=25, y=25)
        access_level = ttk.Label(self, text=admin.access_level)
        access_level.place(x=100, y=25)

        add_employee_button = ttk.Button(self, text="Add employee",
                                         command=lambda: self.create_employee_add_window(admin))
        add_employee_button.place(x=25, y=75)

        add_sick_leave_button = ttk.Button(self, text="Add sick leave",
                                           command=lambda: self.create_sick_leave_add_window(admin))
        add_sick_leave_button.place(x=25, y=120)

        back_button = ttk.Button(self, text="Back", command=self.create_auth_window)
        back_button.place(relx=0.8, rely=0.8)

    def create_sick_leaves_window(self, person):
        self.clear_widgets()
        sick_leaves = app_db.get_sick_leaves(person.id)

        columns = ("start_date", "duration", "illness_type", "salary")
        table = ttk.Treeview(columns=columns, show="headings")
        table.pack(fill=BOTH, expand=1)

        table.heading("start_date", text="start_date")
        table.heading("duration", text='duration')
        table.heading("illness_type", text='illness_type')
        table.heading("salary", text='salary')

        table.column("#1", stretch=NO, width=100)
        table.column("#2", stretch=NO, width=100)
        table.column("#3", stretch=NO, width=100)
        table.column("#4", stretch=NO, width=100)

        data = []
        current = 0
        for item in sick_leaves:
            data.append([])
            data[current].append(item.data()["s"]["start_date"])
            data[current].append(item.data()["s"]["duration"])
            data[current].append(item.data()["s"]["illness_type"])

            date1 = person.start_date
            date2 = item.data()["s"]["start_date"]
            date_diff = (datetime.strptime(date2, '%Y-%m-%d') - datetime.strptime(date1.strftime('%Y-%m-%d'),
                                                                                  '%Y-%m-%d')).days

            print(date_diff)
            salary = person.salary
            if date_diff < 730:
                salary /= 2
            elif 730 <= date_diff <= 1460:
                salary *= 0.8
            data[current].append(salary)

            current += 1

        for item in data:
            table.insert("", END, values=item)

        if isinstance(person, Manager):
            create = self.create_manager_window
        else:
            create = self.create_user_data_window
        button_back = ttk.Button(text="Back", command=lambda: create(person))
        button_back.place(relx=0.8, rely=0.8)

    def create_pensioners_window(self, person):
        self.clear_widgets()

        columns = ("worker_id", "name", "salary", "experience")
        table = ttk.Treeview(columns=columns, show="headings")
        table.pack(fill=BOTH, expand=1)

        table.heading("worker_id", text="worker_id")
        table.heading("name", text='name')
        table.heading("salary", text='salary')
        table.heading("experience", text='experience')

        table.column("#1", stretch=NO, width=100)
        table.column("#2", stretch=NO, width=100)
        table.column("#3", stretch=NO, width=100)
        table.column("#4", stretch=NO, width=100)

        data = app_db.get_pensioners()

        for item in data:
            table.insert("", END, values=item)

        button_back = ttk.Button(text="Back", command=lambda: self.create_manager_window(person))
        button_back.place(relx=0.8, rely=0.8)

    def create_salary_less_than_window(self, salary, person):
        self.clear_widgets()
        data = app_db.get_workers_salary_less_than(salary)

        columns = ("worker_id", "name", "salary", "department")
        table = ttk.Treeview(columns=columns, show="headings")
        table.pack(fill=BOTH, expand=1)

        table.heading("worker_id", text="worker_id")
        table.heading("name", text='name')
        table.heading("salary", text='salary')
        table.heading("department", text='department')

        table.column("#1", stretch=NO, width=100)
        table.column("#2", stretch=NO, width=100)
        table.column("#3", stretch=NO, width=100)
        table.column("#4", stretch=NO, width=100)

        for item in data:
            department = app_db.get_employee_department(item[0])
            item += (department,)
            table.insert("", END, values=item)

        salary_entry = ttk.Entry(self)
        salary_entry.place(x=50, y=200)

        button_refresh = ttk.Button(text="Refresh",
                                    command=lambda: self.create_salary_less_than_window(salary_entry.get(),
                                                                                        person))
        button_refresh.place(x=50, y=225)

        button_back = ttk.Button(text="Back", command=lambda: self.create_manager_window(person))
        button_back.place(relx=0.8, rely=0.8)

    def create_average_age_window(self, department_name, person):
        self.clear_widgets()

        columns = ("average", "department")
        table = ttk.Treeview(columns=columns, show="headings")
        table.pack(fill=BOTH, expand=1)

        table.heading("average", text="average")
        table.heading("department", text="department")

        table.column("#1", stretch=NO, width=100)
        table.column("#2", stretch=NO, width=100)

        graph_data = app_db.get_employees_by_department(department_name)
        ages = []

        for item in graph_data:
            print(item.data()["id"])
            age = app_db.get_employee_age_by_id(item.data()['id'])
            ages.append(age)

        print(ages)
        sum = 0
        for item in ages:
            sum += item[0][0]

        average_age = sum / len(ages)

        table_value = [average_age, department_name]
        data = app_db.get_average_age()

        for item in data:
            print(item)
            table.insert("", END, values=round(item[0], 2))

        table.insert("", END, values=table_value)

        department_entry = ttk.Entry(self)
        department_entry.place(x=50, y=200)

        button_refresh = ttk.Button(text="Refresh",
                                    command=lambda: self.create_average_age_window(department_entry.get(),
                                                                                   person))
        button_refresh.place(x=50, y=225)

        button_back = ttk.Button(text="Back", command=lambda: self.create_manager_window(person))
        button_back.place(relx=0.8, rely=0.8)

    def create_sick_leave_duration_window(self, person):
        self.clear_widgets()

        columns = ("department", "average")
        table = ttk.Treeview(columns=columns, show="headings")
        table.pack(fill=BOTH, expand=1)

        table.heading("department", text="department")
        table.heading("average", text="average")

        table.column("#1", stretch=NO, width=100)
        table.column("#2", stretch=NO, width=100)

        departments = app_db.get_all_departments()
        durations = []
        for item in departments:
            duration = app_db.get_sick_leaves_duration_by_department(item.data()["name"])
            durations.append((item.data()["name"], duration[0].data()["duration"]))

        for item in durations:
            table.insert("", END, values=item)

        button_back = ttk.Button(text="Back", command=lambda: self.create_manager_window(person))
        button_back.place(relx=0.8, rely=0.8)

    def create_average_experience_window(self, person):
        self.clear_widgets()

        columns = ("department", "average")
        table = ttk.Treeview(columns=columns, show="headings")
        table.pack(fill=BOTH, expand=1)

        table.heading("department", text="department")
        table.heading("average", text="average")

        table.column("#1", stretch=NO, width=100)
        table.column("#2", stretch=NO, width=100)

        departments = app_db.get_all_departments()

        general_data = []

        for department in departments:
            graph_data = app_db.get_employees_by_department(department.data()['name'])
            average_exp = 0
            for i in range(len(graph_data)):
                print(graph_data[i].data()['id'])
                try:
                    sql_data = app_db.get_worker_experience_by_department(int(graph_data[i].data()['id']))
                    print("sql_data: ", sql_data)
                    average_exp += sql_data[0][0]
                except TypeError:
                    print('error')
                    continue
            general_data.append((department.data()['name'], round(average_exp / len(graph_data), 2)))
            print()

        print(general_data)
        # data = app_db.get_worker_experience_by_department()
        for item in general_data:
            table.insert("", END, values=item)

        button_back = ttk.Button(text="Back", command=lambda: self.create_manager_window(person))
        button_back.place(relx=0.8, rely=0.8)

    def create_average_salary_window(self, person):
        self.clear_widgets()

        male_label = ttk.Label(text="Men average salary: ")
        male_label.pack()
        self.widgets[AVERAGE_SALARY_MALE_LABEL] = male_label

        columns = ("department", "average")
        male_table = ttk.Treeview(columns=columns, show="headings")
        male_table.pack(fill=BOTH, expand=1)

        male_table.heading("department", text="department")
        male_table.heading("average", text="average")

        male_table.column("#1", stretch=NO, width=100)
        male_table.column("#2", stretch=NO, width=100)

        departments = app_db.get_all_departments()

        general_data = []

        for department in departments:
            graph_data = app_db.get_employees_by_department(department.data()['name'])
            average_exp = 0
            for i in range(len(graph_data)):
                try:
                    sql_data = app_db.get_worker_gender_salary_by_department(int(graph_data[i].data()['id']), 'male')
                    print("sql_data: ", sql_data)
                    average_exp += sql_data[0][0]
                except TypeError:
                    print('error')
                    continue
                except IndexError:
                    continue
            general_data.append((department.data()['name'], round(average_exp / len(graph_data), 2)))
            print()

        print(general_data)
        # data = app_db.get_worker_experience_by_department()
        average_male_salary_by_company = app_db.get_average_salary('female')
        male_table.insert("", END, values=('company', average_male_salary_by_company[0][0]))

        for item in general_data:
            male_table.insert("", END, values=item)

        female_label = ttk.Label(text="Women average salary: ")
        female_label.pack()
        self.widgets[AVERAGE_SALARY_FEMALE_LABEL] = female_label

        columns = ("department", "average")
        female_table = ttk.Treeview(columns=columns, show="headings")
        female_table.pack(fill=BOTH, expand=1)

        female_table.heading("department", text="department")
        female_table.heading("average", text="average")

        female_table.column("#1", stretch=NO, width=100)
        female_table.column("#2", stretch=NO, width=100)

        general_data = []

        for department in departments:
            graph_data = app_db.get_employees_by_department(department.data()['name'])
            average_exp = 0
            for i in range(len(graph_data)):
                try:
                    sql_data = app_db.get_worker_gender_salary_by_department(int(graph_data[i].data()['id']), 'female')
                    print("sql_data: ", sql_data)
                    average_exp += sql_data[0][0]
                except TypeError:
                    print('error')
                    continue
                except IndexError:
                    continue
            general_data.append((department.data()['name'], round(average_exp / len(graph_data), 2)))
            print()

        average_female_salary_by_company = app_db.get_average_salary('female')
        female_table.insert("", END, values=('company', average_female_salary_by_company[0][0]))

        for item in general_data:
            female_table.insert("", END, values=item)

        button_back = ttk.Button(text="Back", command=lambda: self.create_manager_window(person))
        button_back.place(relx=0.8, rely=0.8)

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

        department_label = ttk.Label(text="Department: ")
        department_label.place(x=25, y=150)
        department_entry = ttk.Entry(self)
        department_entry.place(x=100, y=150)
        self.widgets[DEPARTMENT_ENTRY_EMPLOYEE_ADD_WIDGET] = department_entry

        role_label = ttk.Label(text="Role: ")
        role_label.place(x=25, y=175)
        role_entry = ttk.Entry(self)
        role_entry.place(x=100, y=175)
        self.widgets[ROLE_ENTRY_EMPLOYEE_ADD_WIDGET] = role_entry

        birth_year_label = ttk.Label(text="Birth year: ")
        birth_year_label.place(x=25, y=200)
        birth_year_entry = ttk.Entry(self)
        birth_year_entry.place(x=100, y=200)
        self.widgets[BIRTH_YEAR_ENTRY_EMPLOYEE_ADD_WIDGET] = birth_year_entry

        family_state_label = ttk.Label(text="Family state: ")
        family_state_label.place(x=25, y=225)
        family_state_entry = ttk.Entry(self)
        family_state_entry.place(x=100, y=225)
        self.widgets[FAMILY_STATE_ENTRY_EMPLOYEE_ADD_WIDGET] = family_state_entry

        gender_label = ttk.Label(text="Gender: ")
        gender_label.place(x=25, y=250)
        gender_entry = ttk.Entry(self)
        gender_entry.place(x=100, y=250)
        self.widgets[GENDER_ENTRY_EMPLOYEE_ADD_WIDGET] = gender_entry

        kids_amount_label = ttk.Label(text="Kids amount: ")
        kids_amount_label.place(x=25, y=275)
        kids_amount_entry = ttk.Entry(self)
        kids_amount_entry.place(x=100, y=275)
        self.widgets[KIDS_AMOUNT_ENTRY_EMPLOYEE_ADD_WIDGET] = kids_amount_entry

        button_add_employee = ttk.Button(self, text='Add employee',
                                         command=lambda: self.add_employee_button_click(admin))
        button_add_employee.place(x=100, y=300)

        back_button = ttk.Button(self, text="Back", command=lambda: self.create_admin_window(admin))
        back_button.place(relx=0.8, rely=0.8)

    def create_sick_leave_add_window(self, admin):
        self.clear_widgets()

        start_date_label = ttk.Label(self, text="Start date: ")
        start_date_label.place(x=25, y=25)
        start_date_entry = ttk.Entry(self)
        start_date_entry.place(x=100, y=25)
        self.widgets[START_ILLNESS_DATE_WIDGET] = start_date_entry

        duration_label = ttk.Label(self, text="Duration: ")
        duration_label.place(x=25, y=50)
        duration_entry = ttk.Entry(self)
        duration_entry.place(x=100, y=50)
        self.widgets[DURATION_ILLNESS_WIDGET] = duration_entry

        illness_type_label = ttk.Label(self, text="Illness type: ")
        illness_type_label.place(x=25, y=75)
        illness_type_entry = ttk.Entry(self)
        illness_type_entry.place(x=100, y=75)
        self.widgets[ILLNESS_TYPE_WIDGET] = illness_type_entry

        login_label = ttk.Label(self, text="Login: ")
        login_label.place(x=25, y=100)
        login_entry = ttk.Entry(self)
        login_entry.place(x=100, y=100)
        self.widgets[LOGIN_ENTRY_WIDGET_ILLNESS] = login_entry

        button_add_sick_leave = ttk.Button(self, text="Add sick leave",
                                           command=lambda: self.add_sick_leave_button_click(
                                               admin, self.widgets[LOGIN_ENTRY_WIDGET_ILLNESS].get()))
        button_add_sick_leave.place(x=75, y=125)

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
                                  auth_result[1], auth_result[0][0][4], auth_result[0][0][5], auth_result[0][0][6],
                                  auth_result[0][0][7], auth_result[0][0][8])
                self.create_user_data_window(person)
            else:
                person = Manager(auth_result[0][0][0], self.widgets[LOGIN_ENTRY_WIDGET].get(),
                                 self.widgets[PASSWORD_ENTRY_WIDGET].get(), auth_result[0][0][1], auth_result[0][0][2],
                                 auth_result[1], auth_result[0][0][4], auth_result[0][0][5], auth_result[0][0][6],
                                 auth_result[0][0][7], auth_result[0][0][8])
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
        if self.widgets[ROLE_ENTRY_EMPLOYEE_ADD_WIDGET].get() == 'employee':
            employee = Employee(0, self.widgets[LOGIN_ENTRY_EMPLOYEE_ADD_WIDGET].get(),
                                self.widgets[PASSWORD_ENTRY_EMPLOYEE_ADD_WIDGET].get(),
                                self.widgets[NAME_ENTRY_EMPLOYEE_ADD_WIDGET].get(),
                                self.widgets[SALARY_ENTRY_EMPLOYEE_ADD_WIDGET].get(),
                                self.widgets[DEPARTMENT_ENTRY_EMPLOYEE_ADD_WIDGET].get(),
                                self.widgets[BIRTH_YEAR_ENTRY_EMPLOYEE_ADD_WIDGET].get(),
                                "",
                                self.widgets[FAMILY_STATE_ENTRY_EMPLOYEE_ADD_WIDGET].get(),
                                self.widgets[GENDER_ENTRY_EMPLOYEE_ADD_WIDGET].get(),
                                self.widgets[KIDS_AMOUNT_ENTRY_EMPLOYEE_ADD_WIDGET].get())
        else:
            employee = Manager(0, self.widgets[LOGIN_ENTRY_EMPLOYEE_ADD_WIDGET].get(),
                               self.widgets[PASSWORD_ENTRY_EMPLOYEE_ADD_WIDGET].get(),
                               self.widgets[NAME_ENTRY_EMPLOYEE_ADD_WIDGET].get(),
                               self.widgets[SALARY_ENTRY_EMPLOYEE_ADD_WIDGET].get(),
                               self.widgets[DEPARTMENT_ENTRY_EMPLOYEE_ADD_WIDGET].get(),
                               self.widgets[BIRTH_YEAR_ENTRY_EMPLOYEE_ADD_WIDGET].get(),
                               "",
                               self.widgets[FAMILY_STATE_ENTRY_EMPLOYEE_ADD_WIDGET].get(),
                               self.widgets[GENDER_ENTRY_EMPLOYEE_ADD_WIDGET].get(),
                               self.widgets[KIDS_AMOUNT_ENTRY_EMPLOYEE_ADD_WIDGET].get())
        app_db.add_employee(employee)
        self.create_admin_window(admin)

    def add_sick_leave_button_click(self, admin, login):
        sick_leave = SickLeave(self.widgets[START_ILLNESS_DATE_WIDGET].get(),
                               self.widgets[DURATION_ILLNESS_WIDGET].get(),
                               self.widgets[ILLNESS_TYPE_WIDGET].get())
        result = app_db.find_employee_by_login(login)
        app_db.add_sick_leave(result[0][0], sick_leave)
        self.create_admin_window(admin)

    def clear_widgets(self):
        widget_list = self.all_children()
        for item in widget_list:
            item.destroy()

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
