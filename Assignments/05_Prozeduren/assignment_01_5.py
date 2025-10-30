import turtle

def square20():
    for i in range(4):
        turtle.forward(20)
        turtle.right(90)

    turtle.right(90)
    turtle.forward(20)
    turtle.left(90)

def two_squares():
    for i in range(2):
        square20()

def four_squares():
    for i in range(2):
        two_squares()

def eight_squares():
    for i in range(2):
        four_squares()

def sixteen_squares():
    for i in range(2):
        eight_squares()

turtle.speed(50)

turtle.left(90)

sixteen_squares()

turtle.done()