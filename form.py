from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, TelField, SubmitField, PasswordField, BooleanField, DateField, SelectField, IntegerField, DateTimeField
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
aadhaar_regex = r'^[2-9]{1}[0-9]{3}[0-9]{4}[0-9]{4}'
pan_regex = r'^[A-Z]{5}[0-9]{4}[A-Z]{1}'
class TruckRequestForm(FlaskForm):
    pickup_location = StringField('Pickup Location', validators=[DataRequired()]) 
    drop_location = StringField('Drop Location', validators=[DataRequired()])
    truck_type = SelectField('Lorry type Needed', choices=[('open', 'Open'), ('close', 'Closed'), ('container', 'Container'), ('tanker', 'Tanker')], validators=[DataRequired()])
    estimated_weight = IntegerField('Estimated Weight in tons', validators=[DataRequired()])
    submit = SubmitField('Request Lorry')

class TruckRegistrationForm(FlaskForm):
    registration_number = StringField('Registration number', validators=[DataRequired(), Length(min=9, max=10), Regexp(RTO_number_regex, message=("Invalid RTO number"))])
    type = SelectField('Lorry type Needed', choices=[('open', 'Open'), ('close', 'Closed'), ('container', 'Container'), ('tanker', 'Tanker')], validators=[DataRequired()])
    capacity = IntegerField('Max load capacity in tons', validators=[DataRequired()])
    current_location = StringField('Current location from ', validators=[DataRequired()])
    destination_location = StringField('Preferred destination location')
    owner_aadhaar = StringField('Owners Aadhaar number', validators=[Regexp(aadhaar_regex, message=("Write a valid aadhaar number"))])
    owner_name = StringField('Owners name', validators=[Length(min=10)])
    contact_number = TelField('Contact Number', validators=[DataRequired(), Length(min=10)])
    owner_tos = StringField('Owners Terms of Service', validators=[])
    owner_pan = StringField('Owners PAN card number', validators=[Regexp(pan_regex, message="Enter a valid PAN number")])
    available_date = DateField('Date Available', validators=[DataRequired()])
    submit = SubmitField('Request Load')

class MaterialRequestForm(FlaskForm):
    truck_type = SelectField('Lorry type Needed', choices=[('open', 'Open'), ('close', 'Closed'), ('container', 'Container'), ('tanker', 'Tanker')], validators=[DataRequired()])
    capacity = IntegerField('Max load capacity in tons', validators=[DataRequired()])
    current_location = StringField('Current location from ', validators=[DataRequired()])
    destination_location = StringField('Preferred destination location')
    submit = SubmitField('Request Lorry')

class MaterialRegistrationForm(FlaskForm):
    pickup_location = StringField('Pickup Location', validators=[DataRequired()])
    pickup_date = DateField('Pickup date', validators=[DataRequired()])
    pickup_time = SelectField('Pickup time', choices=[('1-12', '01:00 - 12:00'), ('12-00', '12:00 - 00:00')], validators=[DataRequired()])
    drop_location = StringField('Drop Location', validators=[DataRequired()])
    drop_date = DateField('Drop date', validators=[DataRequired()])
    drop_time = SelectField('Drop time', choices=[('1-12', '01:00 - 12:00'), ('12-00', '12:00 - 00:00')], validators=[DataRequired()])
    material_type = StringField('Type of Material', validators=[DataRequired()])
    estimated_weight = IntegerField('Estimated Weight in tons', validators=[DataRequired()])
    truck_type = SelectField('Lorry type Needed', choices=[('open', 'Open'), ('close', 'Closed'), ('container', 'Container'), ('tanker', 'Tanker')], validators=[DataRequired()])
    contact_number = TelField('Contact Number', validators=[DataRequired()])
    submit = SubmitField('Request Lorry')