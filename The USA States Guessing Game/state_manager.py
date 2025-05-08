from turtle import Turtle
FONT = ("Courier", 8, "normal")


class State_manager(Turtle):
    def __init__(self, x, y, state_name):
        super().__init__()
        self.hideturtle()
        self.penup()
        self.goto(x, y)
        self.write(state_name, align="center", font=FONT)

    def non_valid_text(self, answer_state):
        self.write(f"{answer_state} is not a valid state name.", align="center", font=FONT)