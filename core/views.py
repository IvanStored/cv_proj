from flask import Blueprint, redirect, render_template, request, flash
from flask_login import login_user, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms import ValidationError

from core import db, User, Task
from core.forms import RegisterForm, LoginForm, TaskForm

tasks = Blueprint("tasks", __name__)


@tasks.route("/register", methods=["POST", "GET"])
def register():
    form = RegisterForm()
    if request.method == "POST":
        if form.validate_on_submit:
            first_name = form.first_name.data
            last_name = form.last_name.data
            email = form.email.data
            password = generate_password_hash(form.password.data)
            user = User(
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=password,
            )
            db.session.add(user)
            db.session.commit()
            return redirect("/login")
    return render_template("register.html", form=form)


@tasks.route("/login", methods=["POST", "GET"])
def login():
    form = LoginForm()
    if form.validate_on_submit:
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect("/todos")
    return render_template("login.html", form=form)


@tasks.route("/logout", methods=["POST", "GET"])
def logout():
    logout_user()
    return redirect("/")


@tasks.route("/todos", methods=["GET", "POST"])
def todos():
    form = TaskForm()
    if not current_user.is_anonymous:
        todos = Task.query.filter_by(todo_owner=current_user.id).order_by(
            Task.id.desc()
        )
        try:
            if request.method == "POST":
                if form.validate_on_submit:
                    task_name = form.task_name.data
                    due_date = form.due_date.data
                    task = Task(
                        task_name=task_name,
                        due_date=due_date,
                        is_completed=False,
                        todo_owner=current_user.id,
                    )
                    db.session.add(task)
                    db.session.commit()
                    return redirect("/todos")
        except ValidationError:
            flash("Wrong date")
            return redirect("/todos")
        return render_template("todos.html", todos=todos, form=form)

    return redirect("/login")


@tasks.route("/update/<int:id>", methods=["GET"])
def update_status(id):
    if not current_user.is_anonymous:
        task = Task.query.filter_by(id=id, todo_owner=current_user.id).first()
        if task:
            task.is_completed = not task.is_completed
            db.session.commit()

    return redirect("/todos")


@tasks.route("/edit_task/<int:id>", methods=["GET", "POST"])
def edit_task(id):
    if not current_user.is_anonymous:
        form = TaskForm()
        task = Task.query.filter_by(id=id, todo_owner=current_user.id).first()

        if request.method == "POST" and form.validate_on_submit and task:
            task.task_name = form.task_name.data
            task.due_date = form.due_date.data

            db.session.commit()
            return redirect("/todos")
        elif not task:
            return redirect("/todos")
        form.task_name.data = task.task_name
        form.due_date.data = task.due_date
        return render_template("task.html", form=form)
    return render_template("login.html", form=LoginForm())


@tasks.route("/delete_task/<int:id>", methods=["GET", "POST"])
def delete(id):
    if not current_user.is_anonymous:
        task = Task.query.filter_by(id=id, todo_owner=current_user.id).first()
        if task:
            if request.method == "POST":
                db.session.delete(task)
                db.session.commit()
                return redirect("/todos")
            return render_template("delete_task.html")
        else:
            return redirect("/todos")
    return render_template("login.html", form=LoginForm())
