class Person:
    def __init__(self, worker_id, login, password, name):
        self.__id = worker_id
        self.__login = login
        self.__password = password
        self.__name = name

    @property
    def id(self):
        return self.__id

    @property
    def login(self):
        return self.__login

    @property
    def password(self):
        return self.__password

    @property
    def name(self):
        return self.__name

    def __str__(self):
        return self.name


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


class Manager(Employee):
    def __init__(self, worker_id, login, password, name, salary, department, birth_year, start_date, family_state,
                 gender, kids_amount):
        super().__init__(worker_id, login, password, name, salary, department, birth_year, start_date, family_state,
                         gender, kids_amount)


class Admin(Person):
    def __init__(self, worker_id, login, password, name, access_level):
        super().__init__(worker_id, login, password, name)
        self.__access_level = access_level

    @property
    def access_level(self):
        return self.__access_level
