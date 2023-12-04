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
    def __init__(self, worker_id, login, password, name, salary):
        super().__init__(worker_id, login, password, name)
        self.__salary = salary

    @property
    def salary(self):
        return self.__salary


class Admin(Person):
    def __init__(self, worker_id, login, password, name, access_level):
        super().__init__(worker_id, login, password, name)
        self.__access_level = access_level

    @property
    def access_level(self):
        return self.__access_level
