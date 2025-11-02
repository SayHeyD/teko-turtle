import datetime
from typing import Self

class Birthdate:

    def __init__(self, year: int, month: int, day: int):
        self.__year = 0
        self.__month = 0
        self.__day = 0
        self.year(year).month(month).day(day)

    def year(self, year: int) -> Self:
        current_year = datetime.datetime.now().year

        if year < 0:
            raise ValueError("Year cannot be negative")

        if year > datetime.datetime.now().year:
            raise ValueError(f'Year cannot be greater than {current_year}')

        self.__year = year
        return self

    def month(self, month: int) -> Self:
        if month < 1 or month > 12:
            raise ValueError("Month must be between 1 and 12")

        self.__month = month
        return self

    def day(self, day: int) -> Self:
        if day < 1 or day > 31:
            raise ValueError("Day must be between 1 and 31")

        self.__day = day

    def get_year(self):
        return self.__year

    def get_month(self):
        return self.__month

    def get_day(self):
        return self.__day
