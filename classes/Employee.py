from classes.Person import Person


class Employee(Person):
    def __init__(self, worker_id, login, password, name, salary, department, birth_year, start_date, family_state,
                 gender, kids_amount):
        super().__init__(worker_id, login, password, name)
        self.__salary = salary
        self.__department = department
        self.__birth_year = birth_year
        self.__start_date = start_date
        self.__family_state = family_state
        self.__gender = gender
        self.__kids_amount = kids_amount

    @property
    def salary(self):
        return self.__salary

    @property
    def department(self):
        return self.__department

    @property
    def birth_year(self):
        return self.__birth_year

    @property
    def start_date(self):
        return self.__start_date

    @property
    def family_state(self):
        return self.__family_state

    @property
    def gender(self):
        return self.__gender

    @property
    def kids_amount(self):
        return self.__kids_amount