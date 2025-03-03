from turtle import Turtle


class My_Turtle(Turtle):
    def __init__(self):
        super().__init__()
        self.shape("turtle")
        self.color("black")
        self.penup()
        self.left(90)
        self.goto(0, -270)

    def move_forward(self):
        self.forward(10)