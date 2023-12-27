import psycopg2

from classes.Manager import Manager
# from database.database_module import CREATE_SYSTEM_TABLE_QUERY_SQL, CREATE_SALARY_TABLE_QUERY_SQL, \
#     CREATE_ADMIN_TABLE_SQL

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


class SQLDatabase:
    def __init__(self):
        self.conn = psycopg2.connect(dbname="workers", user="postgres", password="postgres", host="127.0.0.1",
                                     port="5432")
        print("Connection enabled")
        self.cursor = self.conn.cursor()
        self.cursor.execute(CREATE_SYSTEM_TABLE_QUERY_SQL)
        self.cursor.execute(CREATE_SALARY_TABLE_QUERY_SQL)
        self.cursor.execute(CREATE_ADMIN_TABLE_SQL)
        self.conn.commit()

    def add_employee(self, employee):
        self.cursor.execute(f'INSERT INTO workers_system_info (login, password) ' +
                            f'VALUES (\'{employee.login}\', {employee.password});')
        last_id = self.get_all()[-1][0]
        if isinstance(employee, Manager):
            role = 'manager'
        else:
            role = 'employee'
        self.cursor.execute(
            f'INSERT INTO workers_salary_info (worker_id, name, salary, role, birth_year, family_state, gender, kids_amount) ' +
            f'VALUES (\'{last_id}\', \'{employee.name}\', {employee.salary}, \'{role}\', {employee.birth_year},'
            f' \'{employee.family_state}\', \'{employee.gender}\', {employee.kids_amount});')
        self.conn.commit()

    def find_employee(self, login, password):
        self.cursor.execute(f"SELECT * FROM workers_system_info WHERE login = '{login}' AND password = '{password}'")
        return self.cursor.fetchall()

    def find_admin(self, login, password):
        self.cursor.execute(f"SELECT * FROM admin_table WHERE login = '{login}' AND password = '{password}'")
        return self.cursor.fetchall()

    def get_all(self):
        self.cursor.execute("SELECT * FROM workers_system_info")
        return self.cursor.fetchall()