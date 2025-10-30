import turtle

def square50():
    for i in range(4):
        turtle.forward(50)
        turtle.left(90)

def row_up(squares):
    turtle.left(180)

    for i in range(squares):
        turtle.forward(50)

    turtle.right(90)
    turtle.forward(50)
    turtle.right(90)

def window():
    for i in range(4):
        for j in range(4):
            square50()
            turtle.forward(50)

        row_up(4)

turtle.speed(50)
window()
turtle.done()