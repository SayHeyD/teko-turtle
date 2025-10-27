from abc import ABC, abstractmethod
import turtle

class Shape(ABC):
    def __init__(self):
        self.__rotation = 0

    def orientation(self, rotation):
        self.__rotation = rotation
        return self

    def rotate(self):
        turtle.right(self.__rotation)

    @abstractmethod
    def render(self):
        pass