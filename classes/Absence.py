class Absence:
    def __init__(self, start_date, duration):
        self.__start_date = start_date
        self.__duration = duration

    @property
    def start_date(self):
        return self.__start_date

    @property
    def duration(self):
        return self.__duration


class SickLeave(Absence):
    def __init__(self, start_date, duration, illness_type):
        super().__init__(start_date, duration)
        self.__illness_type = illness_type

    @property
    def illness_type(self):
        return self.__illness_type

