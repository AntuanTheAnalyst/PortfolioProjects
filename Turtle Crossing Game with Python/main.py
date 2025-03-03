from turtle import Turtle, Screen
from my_turtle import My_Turtle
from car import Car
from scoreboard import Scoreboard
import random
import time

X_COORDINATE = 350


# Screen setup
screen = Screen()
screen.setup(width=600, height=600)
screen.bgcolor("white")
screen.title("My Turtle Crossing Game")
screen.tracer(0)
screen.colormode(255)

# Create player, scoreboard, and cars
my_turtle = My_Turtle()
cars = []  # Dynamic list of cars
scoreboard = Scoreboard()
car_speed = 10 # Initial car speed


# Spawn a new car in a random lane
def spawn_car():
    lane_list = []
    for x in range(-240, 260, 20):
        lane_list.append(x)
    random_lane = random.choice(lane_list)
    cars.append(Car(random_lane, car_speed))


# Keypress event
screen.listen()
screen.onkeypress(my_turtle.move_forward, "w")

# Game loop
game_is_on = True
frame_count = 0  # To control spawning frequency
while game_is_on:
    time.sleep(0.1)
    screen.update()

    # Move all cars forward
    for car in cars:
        car.move_forward()

        # Check for collision with the player
        if my_turtle.distance(car) < 20:
            game_is_on = False
            scoreboard.game_over()

        # Remove car if it goes off-screen
        if car.xcor() < -350:
            cars.remove(car)

    # Check if the player has reached the top of the screen
    if my_turtle.ycor() > 280:
        scoreboard.increase_level()
        my_turtle.goto(0, -270) # Reset the player's position
        car_speed += 5 # Increase car speed for the next level

    # Spawn a new car every few frames
    if frame_count % 4 == 0:  # Adjust frequency as needed
        spawn_car()

    frame_count += 1


screen.exitonclick()
