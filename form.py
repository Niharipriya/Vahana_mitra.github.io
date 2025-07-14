from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, TelField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Email, Length, EqualTo, Regexp

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

RTO_number_regex = r'^[A-Z]{2}[0-9]{2}[A-Z]{1,2}[0-9]{4}'
class TruckRegistrationForm(FlaskForm):
    truck_name = StringField('Truck Owner Name', validators=[DataRequired(), Length(min=5, max=80)])
    truck_registration_number = StringField('Registration Number/RTO Number', validators=[DataRequired(), Regexp(RTO_number_regex, message="Invalid RTO number")])
    availability = BooleanField('Available')
    submit = SubmitField('Add')

class MaterialRegistrationForm(FlaskForm):
    load_name = StringField('Owner of the Materials', validators=[DataRequired(), Length(min=8, max=80)])
    pickup_address = StringField('Material Pick Up Address', validators=[DataRequired()])
    drop_address = StringField('Material Drop off Address', validators=[DataRequired()])
    submit = SubmitField('Add')