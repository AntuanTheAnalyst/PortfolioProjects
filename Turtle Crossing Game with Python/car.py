import turtle
from turtle import Turtle
import random

X_COORDINATE = 350


def random_color():
    """Generate a random RGB color."""
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    return (r, g, b)


class Car(Turtle):
    def __init__(self, y_position, speed):
        super().__init__()
        self.shape("square")
        self.shapesize(stretch_wid=1, stretch_len=2)
        self.color(random_color())
        self.penup()
        self.goto(X_COORDINATE, y_position)
        self.setheading(180)
        self.speed_increment = speed

    def move_forward(self):
        """Move the car forward by the current speed."""
        self.forward(self.speed_increment)








