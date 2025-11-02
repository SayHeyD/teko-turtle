import uuid
from birthdate import Birthdate
from typing import Self

class Student:
    def __init__(self, firstname: str, lastname: str, age: Birthdate, student_id: uuid.UUID|None = None):
        self.__id = student_id
        self.__firstname = None
        self.__lastname = None
        self.__age = None
        self.firstname(firstname).lastname(lastname).age(age)

    def get_id(self) -> uuid.UUID|None:
        return self.__id

    def get_firstname(self) -> str|None:
        return self.__firstname

    def get_lastname(self) -> str|None:
        return self.__lastname

    def get_age(self) -> Birthdate|None:
        return self.__age

    def firstname(self, firstname: str) -> Self:
        self.__firstname = firstname
        return self

    def lastname(self, lastname: str) -> Self:
        self.__lastname = lastname
        return self

    def age(self, age: Birthdate) -> Self:
        self.__age = age
        return self

    def to_array(self) -> list[str|int|uuid.UUID]:

        if self.__id is None:
            self.__id = uuid.uuid4()

        return [
            self.get_id(),
            self.get_firstname(),
            self.get_lastname(),
            self.get_age().get_year(),
            self.get_age().get_month(),
            self.get_age().get_day()
        ]