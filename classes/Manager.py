from classes.Employee import Employee


class Manager(Employee):
    def __init__(self, worker_id, login, password, name, salary, department, birth_year, start_date, family_state,
                 gender, kids_amount):
        super().__init__(worker_id, login, password, name, salary, department, birth_year, start_date, family_state,
                         gender, kids_amount)