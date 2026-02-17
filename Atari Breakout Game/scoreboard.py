from turtle import Turtle


class Scoreboard(Turtle):
    def __init__(self):
        super().__init__()
        self.color("white")
        self.penup()
        self.hideturtle()
        self.score = 0
        self.update_score()

    def update_score(self):
        """Update the scoreboard with the current level."""
        self.clear()
        self.goto(0, 255)
        self.write(f"Score: {self.score}", align="center", font=("Courier", 15, "normal"))

    def increase_score(self):
        """Increase the level by 500."""
        self.score += 500
        self.update_score()

    def reset_score(self):
        self.score = 0
        self.update_score()

    def show_start_message(self):
        self.goto(0, 20)
        self.write("Press SPACE to Start",
                   align="center",
                   font=("Arial", 24, "bold"))

    def game_over(self):
        """Display 'Game Over' on the screen."""
        self.goto(0, 0)
        self.write(f"GAME OVER", align="center", font=("Courier", 25, "bold"))
        self.goto(0,-40)
        self.write(f"Press R to restart", align="center", font=("Courier", 25, "bold"))


