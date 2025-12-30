from turtle import Turtle


class Scoreboard(Turtle):
    def __init__(self):
        super().__init__()
        self.color("black")
        self.penup()
        self.hideturtle()
        self.level = 1
        self.update_score()

    def update_score(self):
        """Update the scoreboard with the current level."""
        self.clear()
        self.goto(-230, 255)
        self.write(f"Level: {self.level}", align="center", font=("Courier", 15, "normal"))

    def increase_level(self):
        """Increase the level by 1."""
        self.level += 1
        self.update_score()

    def game_over(self):
        """Display 'Game Over' on the screen."""
        self.goto(0, 0)
        self.write(f"Game Over", align="center", font=("Courier", 25, "bold"))