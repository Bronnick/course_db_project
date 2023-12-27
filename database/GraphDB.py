import neo4j.exceptions
from neo4j import GraphDatabase

# from database.database_module import department_names
department_names = ['financial', 'staff', 'improvement']

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
    def get_sick_leaves_duration_by_department(tx, department_name):
        result = tx.run("MATCH (d:Department{name:$department_name})-[r:works_in]-(e:Employee)-[h:has_illness]-(s:SickLeave)"
                        "RETURN SUM(toInteger(s.duration)) AS duration", department_name=department_name)
        return result.fetch(100)

    @staticmethod
    def get_all_departments(tx):
        result = tx.run('MATCH (d:Department) RETURN d.name AS name')
        return result.fetch(100)

    @staticmethod
    def _get_all(tx):
        result = tx.run("MATCH (n) RETURN (n)")
        return result.fetch(100)