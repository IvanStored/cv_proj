from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    EmailField,
    PasswordField,
    SubmitField,
    DateField,
)
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    first_name = StringField("First name", validators=[DataRequired()])
    last_name = StringField("Last name", validators=[DataRequired()])
    email = EmailField("Email", validators=[DataRequired()])
    password = PasswordField("Email", validators=[DataRequired()])
    submit = SubmitField("Register")


class LoginForm(FlaskForm):
    email = EmailField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Sign in")


class TaskForm(FlaskForm):
    task_name = StringField("Name", validators=[DataRequired()])
    due_date = DateField("Due Date", validators=[DataRequired()])
    submit = SubmitField("Submit")
