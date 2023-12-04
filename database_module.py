import neo4j.exceptions
import psycopg2
from neo4j import GraphDatabase

CREATE_SALARY_TABLE_QUERY_SQL = "CREATE TABLE IF NOT EXISTS " \
                                "workers_salary_info(worker_id INTEGER REFERENCES workers_system_info ," \
                                "name TEXT, " \
                                "salary FLOAT);"

CREATE_SYSTEM_TABLE_QUERY_SQL = "CREATE TABLE IF NOT EXISTS " \
                                "workers_system_info(worker_id SERIAL PRIMARY KEY, login TEXT UNIQUE, password TEXT," \
                                "role TEXT CHECK (role = 'manager' or role = 'admin' or role = 'employee'));"

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
            session.execute_write(GraphDB.add_employee, last_id)

    def authenticate_employee(self, login, password, is_admin):
        try:
            if is_admin == 0:
                print("workers salary exec")
                self.sql_database.cursor.execute(
                    f'SELECT * FROM workers_salary_info WHERE worker_id = {self.sql_database.find_employee(login, password)[0][0]}')
            else:
                self.sql_database.cursor.execute(
                    f'SELECT * FROM admin_table WHERE admin_id = {self.sql_database.find_admin(login, password)[0][0]}')
            return self.sql_database.cursor.fetchall()
        except IndexError:
            return -1


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
        self.cursor.execute(f'INSERT INTO workers_salary_info (worker_id, name, salary) ' +
                            f'VALUES (\'{last_id}\', \'{employee.name}\', {employee.salary});')
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
    def add_employee(tx, employee_id):
        tx.run("CREATE (e:Employee) "
               "SET e.employee_id = $id ", id=employee_id)

    @staticmethod
    def _create_departments(tx):
        for name in department_names:
            tx.run("CREATE (d:Department) "
                   "SET d.name = $message", message=name)

    @staticmethod
    def _get_all(tx):
        result = tx.run("MATCH (n) RETURN (n)")
        return result.fetch(100)
