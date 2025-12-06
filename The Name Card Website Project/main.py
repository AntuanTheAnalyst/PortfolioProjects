from flask import Flask, render_template

app = Flask(__name__)
print(app)

@app.route("/")
def home():
    return render_template("index_personal_site.html")


if __name__ == "__main__":
    app.run()

