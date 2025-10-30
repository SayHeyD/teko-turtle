import turtle

def square20():
    for _ in range(4):
        turtle.forward(20)
        turtle.right(90)

    turtle.right(90)
    turtle.forward(20)
    turtle.left(90)

turtle.speed(50)

turtle.left(90)

# Anstatt eine Kombination aus den Funktionen zu nutzen, sollten wir einfach
# die square20() funktion so oft aufrufen wie nötig, also 13 oder 17 mal

squares = 17

for i in range(squares):
    square20()

turtle.done()