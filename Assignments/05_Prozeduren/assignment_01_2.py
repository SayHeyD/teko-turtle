import turtle

def open_square():
    turtle.left(90)
    turtle.forward(100)

    for i in range(2):
        turtle.right(90)
        turtle.forward(100)

turtle.speed(50)

for i in range(4):
    open_square()

turtle.done()
