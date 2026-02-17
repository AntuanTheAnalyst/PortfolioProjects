from turtle import Turtle


class Paddle(Turtle):
    def __init__(self):
        super().__init__()
        self.shape("square")
        self.color("white")
        self.shapesize(stretch_wid=1, stretch_len=5)  # Stretch shape to make it a paddle
        self.penup()  # No drawing when moving
        self.goto(0, -250)  # Starting position

    # Functions to move the paddle
    def move_right(self):
        x = self.xcor()  # Get the current x-coordinate
        if x < 340:  # Prevent going off screen
            self.setx(x + 20)

    def move_left(self):
        x = self.xcor()
        if x > -345:
            self.setx(x - 20)
