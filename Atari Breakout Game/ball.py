from turtle import Turtle


class Ball(Turtle):
    def __init__(self):
        super().__init__()
        self.shape("circle")
        self.speed(40)  # Initial animation speed
        self.color("white")
        self.penup()
        self.goto(0, 0)  # Start in the center
        self.dx = 5.5  # Movement increment in the x-direction
        self.dy = 5.5  # Movement increment in the y-direction

    def move(self):
        # Update ball position
        x = self.xcor() + self.dx
        y = self.ycor() + self.dy
        self.goto(x, y)

        if self.ycor() > 285 or self.ycor() < -285:
            self.dy *= -1

        if self.xcor() > 385 or self.xcor() < -385:
            self.dx *= -1

    # def check_collision_with_paddle(self, paddle):
    #     # Check if ball is near paddle vertically
    #     if -230 > self.ycor() > -260:
    #         # Check if ball is inside paddle width
    #         if paddle.xcor() - 50 < self.xcor() < paddle.xcor() + 50:
    #             self.dy *= -1

    def check_collision_with_paddle(self, paddle):
        # only collide if moving downward
        if self.dy < 0:

            if (paddle.ycor() - 10 < self.ycor() < paddle.ycor() + 10 and
                    paddle.xcor() - 50 < self.xcor() < paddle.xcor() + 50):
                # bounce upward
                self.dy = abs(self.dy)

                # push ball above paddle to prevent sticking
                self.sety(paddle.ycor() + 20)

                # optional: angle control based on hit position
                offset = (self.xcor() - paddle.xcor()) / 50
                self.dx += offset * 1.5



