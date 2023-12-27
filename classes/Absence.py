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


