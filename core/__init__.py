from datetime import datetime

from flask import Flask, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from sqlalchemy.orm import validates
from wtforms import ValidationError

app = Flask(__name__, template_folder="templates")
SECRET_KEY = "some secret key"
app.config["SECRET_KEY"] = SECRET_KEY
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///mydb.sqlite3"
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String)
    todos = db.relationship("Task", backref="owner")

    def __repr__(self):
        return f"User{self.first_name}{self.email}"

    @property
    def is_active(self):
        return True

    @property
    def is_authenticated(self):
        return self.is_active

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return str(self.id)
        except AttributeError:
            raise NotImplementedError(
                "No `id` attribute - override `get_id`"
            ) from None


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task_name = db.Column(db.String(255))
    due_date = db.Column(db.DateTime())
    is_completed = db.Column(db.Boolean)
    todo_owner = db.Column(db.Integer, db.ForeignKey("user.id"))

    def __repr__(self):
        return f"Task {self.task_name} is {self.is_completed}"

    @validates("due_date")
    def validate_due_date(self, key, due_date):
        if due_date < datetime.date(datetime.today()):
            raise ValidationError()

        return due_date


from core.views import tasks

with app.app_context():

    db.create_all()


@app.route("/")
def home():
    return redirect("/todos")


login_manager = LoginManager()

login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


app.register_blueprint(tasks)
