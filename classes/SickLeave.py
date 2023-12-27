from classes.Absence import Absence


class SickLeave(Absence):
    def __init__(self, start_date, duration, illness_type):
        super().__init__(start_date, duration)
        self.__illness_type = illness_type

    @property
    def illness_type(self):
        return self.__illness_type
