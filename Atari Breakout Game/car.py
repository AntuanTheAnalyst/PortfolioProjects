import turtle
from turtle import Turtle
import random


class Car(Turtle):
    def __init__(self, x, y, color):
        super().__init__()
        self.shape("square")
        self.shapesize(stretch_wid=1, stretch_len=3)
        self.color(color)
        self.penup()
        self.goto(x, y)


