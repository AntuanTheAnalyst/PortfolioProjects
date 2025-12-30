from flask import Flask
import random

app = Flask(__name__)


@app.route("/")
def home():
    return ("<h1>Guess a number between 0 and 9 </h1>"
            "<img src='https://i.giphy.com/3o7aCSPqXE5C6T8tBC.webp'>")


random_number = random.randint(0, 9)
print(random_number)


def too_low():
    return (f"<h1 style='color:red'><b>Too low, try again!</b></h1>"
            f"<img src='https://media.giphy.com/media/jD4DwBtqPXRXa/giphy.gif'>")


def too_high():
    return (f"<h1 style='color:purple'><b>Too high, try again!</b></h1>"
            f"<img src='https://media.giphy.com/media/3o6ZtaO9BZHcOjmErm/giphy.gif'>")


def correct():
    return (f"<h1 style='color:green'><b>You found me!</b></h1>"
            f"<img src='https://media.giphy.com/media/4T7e4DmcrP9du/giphy.gif'>")


@app.route("/<int:guess>")
def user_guess(guess):
    if guess > random_number:
        return too_high()
    elif guess < random_number:
        return too_low()
    elif random_number == guess:
        return correct()


if __name__ == "__main__":
    app.run(debug=True)
