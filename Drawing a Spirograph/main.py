import turtle
import random

# Set up the screen
screen = turtle.Screen()
screen.bgcolor("black")

# Create the turtle
spiro_turtle = turtle.Turtle()
spiro_turtle.speed("fastest")  # Fast drawing speed

# Function to generate a random color
def random_color():
    r = random.random()
    g = random.random()
    b = random.random()
    return (r, g, b)

# Set the turtle to use RGB colors
turtle.colormode(1.0)

# Draw spirograph
def draw_spirograph(radius, step):
    for _ in range(int(360 / step)):
        spiro_turtle.color(random_color())  # Set a random color
        spiro_turtle.circle(radius)        # Draw a circle
        spiro_turtle.right(step)           # Tilt the circle

# Draw a spirograph with a radius of 100 and tilt step of 10 degrees
draw_spirograph(radius=100, step=10)

# Hide the turtle and display the result
spiro_turtle.hideturtle()
screen.mainloop()
