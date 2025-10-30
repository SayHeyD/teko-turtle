def point_in_circle(x_coordinate: int, y_coordinate: int, radius: int) -> bool:
    # Distanz des Punktes zur Mitte des Kreises (pythagoras),
    # wenn also r unsere Hypotenuse ist, muss x^2 + y^2 kleiner sein
    # als radius^2, da ansonsten der Satz des Pythagoras nicht erfüllt ist
    return x_coordinate**2 + y_coordinate**2 <= radius**2


points_to_check = [
    [2, 3, 4, True],
    [2, 3, 3, False],
    [-2, 1, 3, True],
    [-3, -4, 7, True],
    [-4, -6, 7, False]
]

for point in points_to_check:
    print(f'Punkt: ({point[0]}, {point[1]}), Radius: {point[2]}, In Kreis: {point_in_circle(point[0], point[1], point[2])}')