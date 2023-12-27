from database.GraphDB import GraphDB
from database.SQLDatabase import SQLDatabase

CREATE_SALARY_TABLE_QUERY_SQL = "CREATE TABLE IF NOT EXISTS " \
                                "workers_salary_info(worker_id INTEGER REFERENCES workers_system_info ," \
                                "name TEXT, " \
                                "salary FLOAT, " \
                                "role TEXT CHECK (role = 'manager' or role = 'admin' or role = 'employee'), " \
                                "birth_year INTEGER, " \
                                "start_date DATE DEFAULT CURRENT_DATE, " \
                                "family_state TEXT CHECK (family_state = 'married' or family_state = 'not married'), " \
                                "gender TEXT CHECK (gender = 'male' or gender = 'female'), " \
                                "kids_amount INTEGER " \
                                ");"

CREATE_SYSTEM_TABLE_QUERY_SQL = "CREATE TABLE IF NOT EXISTS " \
                                "workers_system_info(worker_id SERIAL PRIMARY KEY, login TEXT UNIQUE, password TEXT" \
                                ");"

CREATE_ADMIN_TABLE_SQL = "CREATE TABLE IF NOT EXISTS admin_table (admin_id SERIAL PRIMARY KEY," \
                         "login TEXT UNIQUE, password TEXT, access_level INTEGER);"

department_names = ['financial', 'staff', 'improvement']


class AppDatabase:
    def __init__(self):
        self.sql_database = SQLDatabase()
        self.graph_database = GraphDB()

    def add_employee(self, employee):
        self.sql_database.add_employee(employee)
        employees = self.sql_database.get_all()
        last_id = employees[-1][0]
        with self.graph_database.driver.session() as session:
            session.execute_write(GraphDB.add_employee, last_id, employee.department)

    def add_sick_leave(self, _id, sick_leave):
        with self.graph_database.driver.session() as session:
            session.execute_write(GraphDB.add_sick_leave, _id, sick_leave)

    def get_all_employees(self):
        data = []
        self.sql_database.cursor.execute(f'SELECT * FROM workers_salary_info')
        sql_data = self.sql_database.cursor.fetchall()
        for item in sql_data:
            with self.graph_database.driver.session() as session:
                graph_data = session.execute_write(GraphDB.find_department, item[0])
                current = [item, graph_data]
                data.append(current)
        return data

    def authenticate_employee(self, login, password, is_admin):
        try:
            if is_admin == 0:
                self.sql_database.cursor.execute(
                    f'SELECT * FROM workers_salary_info WHERE worker_id = {self.sql_database.find_employee(login, password)[0][0]}')
                sql_data = self.sql_database.cursor.fetchall()
                with self.graph_database.driver.session() as session:
                    graph_data = session.execute_write(GraphDB.find_department, sql_data[0][0])
                return sql_data, graph_data[0].data()["name"]
            else:
                self.sql_database.cursor.execute(
                    f'SELECT * FROM admin_table WHERE admin_id = {self.sql_database.find_admin(login, password)[0][0]}')
                sql_data = self.sql_database.cursor.fetchall()
                return sql_data
        except IndexError:
            return -1

    def find_employee_by_login(self, login):
        self.sql_database.cursor.execute(
            f"SELECT worker_id FROM workers_system_info WHERE login = \'{login}\'; ")
        return self.sql_database.cursor.fetchall()

    def get_sick_leaves(self, employee_id):
        with self.graph_database.driver.session() as session:
            graph_data = session.execute_write(GraphDB.get_sick_leaves_by_id, employee_id)
            return graph_data

    def get_pensioners(self):
        self.sql_database.cursor.execute("SELECT worker_id, name, salary, "
                                         "(DATE_PART('year', CURRENT_DATE) - DATE_PART('year', start_date)) as experience "
                                         "FROM workers_salary_info WHERE (EXTRACT(YEAR FROM CURRENT_DATE) - birth_year) > 60;")
        return self.sql_database.cursor.fetchall()

    def get_workers_salary_less_than(self, salary):
        self.sql_database.cursor.execute(f"SELECT worker_id, name, salary FROM workers_salary_info "
                                         f"WHERE salary < {salary};")
        return self.sql_database.cursor.fetchall()

    def get_employee_department(self, employee_id):
        with self.graph_database.driver.session() as session:
            graph_data = session.execute_write(GraphDB.find_department, employee_id)
            return graph_data[0].data()["name"]

    def get_average_age(self):
        self.sql_database.cursor.execute("SELECT AVG(DATE_PART('year', CURRENT_DATE) - birth_year) "
                                         "FROM workers_salary_info;")
        return self.sql_database.cursor.fetchall()

    def get_employees_by_department(self, department_name: str):
        with self.graph_database.driver.session() as session:
            graph_data = session.execute_write(GraphDB.get_employees_by_department, department_name)
            return graph_data

    def get_employee_age_by_id(self, _id):
        self.sql_database.cursor.execute("SELECT DATE_PART('year', CURRENT_DATE) - birth_year "
                                         f"FROM workers_salary_info WHERE worker_id = {_id};")
        return self.sql_database.cursor.fetchall()

    def get_all_departments(self):
        with self.graph_database.driver.session() as session:
            graph_data = session.execute_write(GraphDB.get_all_departments)
            return graph_data

    def get_sick_leaves_duration_by_department(self, department_name):
        with self.graph_database.driver.session() as session:
            graph_data = session.execute_write(GraphDB.get_sick_leaves_duration_by_department, department_name)
            return graph_data

    def get_worker_experience_by_department(self, worker_id):
        self.sql_database.cursor.execute("SELECT (DATE_PART('year', CURRENT_DATE) - DATE_PART('year', start_date)) as experience "
                                         "FROM workers_salary_info "
                                         f"WHERE worker_id={worker_id}")
        return self.sql_database.cursor.fetchall()

    def get_average_salary(self, gender):
        self.sql_database.cursor.execute(
            f"SELECT AVG(salary) FROM workers_salary_info WHERE gender=\'{gender}\';"
        )
        return self.sql_database.cursor.fetchall()

    def get_worker_gender_salary_by_department(self, worker_id, gender):
        self.sql_database.cursor.execute(
            "SELECT salary "
            "FROM workers_salary_info "
            f"WHERE worker_id={worker_id} AND gender=\'{gender}\'")
        return self.sql_database.cursor.fetchall()

    def increase_salary(self, login, amount):
        self.sql_database.cursor.execute(
            f"SELECT worker_id FROM workers_system_info WHERE login=\'{login}\'"
        )
        worker_id = self.sql_database.cursor.fetchall()[0][0]
        self.sql_database.cursor.execute(
            "UPDATE workers_salary_info "
            f"SET salary=salary+{amount} WHERE worker_id={worker_id}"
        )
        self.sql_database.conn.commit()


