import string

import neo4j.exceptions
import psycopg2
from neo4j import GraphDatabase

from classes.Person import Manager
from classes.Absence import SickLeave

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
        self.sql_database.cursor.execute(
            f'SELECT * FROM workers_salary_info')
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
        role = ''
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


class GraphDB:
    def __init__(self):
        self.driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "Murchick228"))
        with self.driver.session() as session:
            try:
                res = session.execute_write(self._get_all)
                if res.count() == 0:
                    session.execute_write(self._create_departments)
                else:
                    for item in res:
                        print(item.data()['n']['name'])
            except TypeError:
                try:
                    session.execute_write(self._create_departments)
                except neo4j.exceptions.ConstraintError:
                    print("node already exists")

    @staticmethod
    def add_employee(tx, employee_id, department_name):
        tx.run("CREATE (e:Employee) "
               "SET e.employee_id = $id ", id=employee_id)
        tx.run("MATCH(e:Employee{employee_id: $id}), "
               "(d:Department{name:$name}) "
               "CREATE (e)-[r:works_in]->(d)", id=employee_id, name=department_name)

    @staticmethod
    def add_sick_leave(tx, employee_id, sick_leave):
        tx.run("CREATE (s:SickLeave) "
               "SET s.start_date = $start_date "
               "SET s.duration = $duration "
               "SET s.illness_type = $illness_type ", start_date=sick_leave.start_date,
               duration=sick_leave.duration, illness_type=sick_leave.illness_type)
        tx.run("MATCH(e:Employee{employee_id: $id}), "
               "(s:SickLeave{start_date:$date, duration:$duration, illness_type:$illness_type}) "
               "CREATE (e)-[r:has_illness]->(s)", id=employee_id, date=sick_leave.start_date,
               duration=sick_leave.duration, illness_type=sick_leave.illness_type)

    def get_employee_department(self):
        pass

    @staticmethod
    def _create_departments(tx):
        for name in department_names:
            tx.run("CREATE (d:Department) "
                   "SET d.name = $message", message=name)

    @staticmethod
    def find_department(tx, employee_id):
        result = tx.run("MATCH path = (e:Employee{employee_id: $id})-[r:works_in]-(d:Department) "
                        "RETURN d.name AS name", id=employee_id)
        return result.fetch(1)

    @staticmethod
    def get_sick_leaves_by_id(tx, employee_id):
        result = tx.run("MATCH path = (e:Employee{employee_id: $id})-[r:has_illness]-(s:SickLeave) "
                        "RETURN s", id=employee_id)
        return result.fetch(100)

    @staticmethod
    def get_employees_by_department(tx, department_name):
        result = tx.run('MATCH paths = (e:Employee)-[r:works_in]-(d:Department{name: $department_name}) '
                        "RETURN e.employee_id AS id", department_name=department_name)
        return result.fetch(100)

    @staticmethod
    def _get_all(tx):
        result = tx.run("MATCH (n) RETURN (n)")
        return result.fetch(100)
