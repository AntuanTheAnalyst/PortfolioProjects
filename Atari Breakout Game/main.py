from turtle import Turtle, Screen
from paddle import Paddle
from ball import Ball
from car import Car
from scoreboard import Scoreboard
import time
import random

ball_active = False

cars = []


# Screen setup
screen = Screen()
screen.setup(width=800, height=600)
screen.bgcolor("black")
screen.title("Atari Breakout Game")
screen.tracer(0)
screen.colormode(255)

ball = Ball()
paddle = Paddle()
scoreboard = Scoreboard()


def deploy_bricks():
    colors = ["blue", "red", "yellow", "green"]
    start_y = 220
    spawn_y = 320  # start above the screen

    for row in range(4):
        target_y = start_y - row * 40

        for x in range(-300, 301, 65):
            car = Car(x, spawn_y, colors[row])
            car.target_y = target_y
            car.falling = True  # mark it as falling
            cars.append(car)


def start_ball():
    global ball_active
    ball_active = True
    scoreboard.clear()


def reset_game():
    global game_is_on, cars, ball_active

    ball_active = False  # stop the ball until space is pressed
    game_is_on = True

    # Clear old bricks
    for car in cars[:]:
        car.hideturtle()
    cars.clear()

    # Reset ball and paddle
    ball.goto(0, 0)
    ball.dx = 5.5
    ball.dy = 5.5
    paddle.goto(0, -250)

    # Reset scoreboard
    scoreboard.reset_score()
    scoreboard.show_start_message()  # show the "Press SPACE to Start" message

    # Recreate bricks
    deploy_bricks()



# Keyboard bindings
screen.listen()
screen.onkeypress(paddle.move_left, "a")
screen.onkeypress(paddle.move_right, "d")
screen.onkeypress(reset_game, "r")
screen.onkeypress(start_ball, "space")

scoreboard.show_start_message()
deploy_bricks()
game_is_on = True
while True:
    time.sleep(0.02)
    screen.update()

    if game_is_on:
        # Animate falling bricks
        for car in cars:
            if getattr(car, "falling", False):
                if car.ycor() > car.target_y:
                    car.sety(car.ycor() - 5)
                else:
                    car.falling = False

        # Only move ball if player pressed space
        if ball_active:
            ball.move()
            ball.check_collision_with_paddle(paddle)

        for car in cars[:]:
            if getattr(car, "falling", False):
                continue  # skip falling bricks

            if ball.distance(car) < 35:
                car.hideturtle()
                cars.remove(car)
                scoreboard.increase_score()
                ball.dy *= -1

    if len(cars) == 0:
        deploy_bricks()

    if ball.ycor() < -280:
        game_is_on = False
        scoreboard.game_over()


screen.mainloop()

