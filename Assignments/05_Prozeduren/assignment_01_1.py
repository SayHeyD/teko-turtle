import turtle

def triangle100():
    for i in range(3):
        turtle.left(120)
        turtle.forward(100)

turtle.speed(50)

for i in range(6):
    triangle100()
    turtle.left(60)

turtle.done()