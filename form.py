from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, TelField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Email, Length, EqualTo

class SignupForm(FlaskForm):
    fullname = StringField('Full Name', validators=[DataRequired(), Length(min=2, max=80)])
    phone = TelField('Phone Number', validators=[DataRequired(), Length(min=10)])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    submit = SubmitField('Signup')

class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    submit = SubmitField('Login')