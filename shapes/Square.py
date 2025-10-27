from .Shape import Shape
import turtle

class Square(Shape):

    __corners = 4
    __corner_angle = 90

    def __init__(self):
        super().__init__()
        self.__length = 0

    @staticmethod
    def build():
        return Square()

    @staticmethod
    def get_corners():
        return Square.__corners

    @staticmethod
    def get_corner_angle():
        return Square.__corner_angle

    def side_length(self, length):
        self.__length = length
        return self

    def render(self):
        self.rotate()

        for i in range(self.__corners):
            turtle.forward(self.__length)
            turtle.right(self.__corner_angle)
            pass