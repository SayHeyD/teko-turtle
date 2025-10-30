import turtle

def square50():
    for i in range(4):
        turtle.forward(50)
        turtle.left(90)

def row_up():
    turtle.left(90)
    turtle.forward(100)
    turtle.left(90)


def window():
    for i in range(2):

        for j in range(2):
            square50()
            turtle.forward(50)

        row_up()

turtle.speed(50)
window()
turtle.done()