from classes.Person import Person


class Admin(Person):
    def __init__(self, worker_id, login, password, name, access_level):
        super().__init__(worker_id, login, password, name)
        self.__access_level = access_level

    @property
    def access_level(self):
        return self.__access_level