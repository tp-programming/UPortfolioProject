from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import InputRequired, Email, Length


class RegisterForm(FlaskForm):
    email = StringField(validators=[InputRequired(), Email()])
    firstname = StringField(validators=[InputRequired()])
    password = PasswordField(validators=[InputRequired()])
    confirm_password = PasswordField(validators=[InputRequired(), Length(min=6, max=12, message="Passwords Must Be Between 6-12 Characters In Length.")])
    submit = SubmitField()

class LoginForm(FlaskForm):
    email = StringField(validators=[InputRequired(), Email()])
    password = PasswordField(validators=[InputRequired()])
    submit = SubmitField()