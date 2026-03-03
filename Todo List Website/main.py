from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todo.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Boolean, default=False)
    due_date = db.Column(db.Date, nullable=True)

    def __repr__(self):
        return f"<Task {self.id}"


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        task_content = request.form.get("task")
        due_date_str = request.form.get("due_date")

        due_date = None
        if due_date_str:
            due_date = datetime.strptime(due_date_str, "%Y-%m-%d").date()

        if task_content:
            new_task = Task(content=task_content, due_date=due_date)
            db.session.add(new_task)
            db.session.commit()

            return redirect(url_for("home"))

    tasks = Task.query.order_by(Task.id.desc()).all()

    total_tasks = len(tasks)
    completed_tasks = sum(1 for task in tasks if task.completed)

    return render_template(
        "index.html",
        tasks=tasks,
        total_tasks=total_tasks,
        completed_tasks=completed_tasks,
        date=date
    )


@app.route("/delete/<int:id>")
def delete(id):
    task = Task.query.get_or_404(id)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for("home"))


@app.route("/complete/<int:id>")
def complete(id):
    task = Task.query.get_or_404(id)
    task.completed = not task.completed
    db.session.commit()
    return redirect(url_for("home"))


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)