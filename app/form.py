from app.support_wtform import IntlTelInput
from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, TelField, SubmitField, PasswordField, BooleanField, DateField, SelectField, IntegerField
from wtforms import HiddenField, TextAreaField, DateTimeField, FileField
from wtforms.validators import DataRequired, Email, Length, EqualTo, Regexp

class SignupForm(FlaskForm):
    fullname = StringField('Full Name', validators=[DataRequired(), Length(min=2, max=80)])
    phone = StringField('Phone Number', validators=[DataRequired(), Length(min=10)], widget=IntlTelInput())
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password_hash = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    submit = SubmitField('Signup')

class LoginForm(FlaskForm):
    phone = StringField('Phone Number', validators=[DataRequired(), Length(min=10)], widget=IntlTelInput())
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
    user_fullname = StringField('Full Name', validators=[DataRequired(), Length(min=2, max=80)])
    user_phone = StringField('Phone Number', validators=[DataRequired(), Length(min=10, max=20)], widget=IntlTelInput())
    user_email = EmailField('Email', validators=[DataRequired(), Email()])

    registration_number = StringField('Registration number', validators=[DataRequired(), Length(min=9, max=10), Regexp(RTO_number_regex, message=("Invalid RTO number"))])
    model_name = StringField('Trucks Model', validators=[DataRequired()])
    type = SelectField('Lorry type Needed', choices=[('open', 'Open'), ('close', 'Closed'), ('container', 'Container'), ('tanker', 'Tanker')], validators=[DataRequired()])
    capacity = IntegerField('Max load capacity in tons', validators=[DataRequired()])
    current_location = StringField('Current location from ', validators=[DataRequired()])
    available_locations = StringField('Preferred destination location')

    owner_name = StringField('Owners name', validators=[Length(min=10)])
    owner_phone = StringField('Phone Number', validators=[Length(min=10, max=20)], widget=IntlTelInput())
    owner_aadhaar = StringField('Owners Aadhaar number', validators=[Regexp(aadhaar_regex, message=("Write a valid aadhaar number"))])
    owner_pan = StringField('Owners PAN card number', validators=[Regexp(pan_regex, message="Enter a valid PAN number")])

    driver_name = StringField('Driver Name')
    driver_aadhaar = StringField('Driver Aadhaar')
    driver_license = FileField('Driver Driving License')

    vehicle_insurance = FileField('Vehicle Insurance')
    available_date = DateField('Date Available')
    submit = SubmitField('Register Truck')

class LoadRequestForm(FlaskForm):
    truck_type = SelectField('Lorry type Needed', choices=[('open', 'Open'), ('close', 'Closed'), ('container', 'Container'), ('tanker', 'Tanker')], validators=[DataRequired()])
    capacity = IntegerField('Max load capacity in tons', validators=[DataRequired()])
    current_location = StringField('Current location from ', validators=[DataRequired()])
    destination_location = StringField('Preferred destination location')
    submit = SubmitField('Request Lorry')

class LoadRegistrationForm(FlaskForm):
    user_fullname = StringField('Full Name', validators=[DataRequired(), Length(min=2, max=80)])
    user_phone = StringField('Phone Number', validators=[DataRequired(), Length(min=10, max=20)], widget=IntlTelInput())
    user_email = EmailField('Email', validators=[DataRequired(), Email()])

    pickup_location = StringField('Pickup Location', validators=[DataRequired()])
    pickup_date = DateField('Pickup date', validators=[DataRequired()])
    pickup_contact_name = StringField('Full Name', validators=[Length(min=2, max=80)])
    pickup_contact_phone = StringField('Phone Number', validators=[Length(min=10)], widget=IntlTelInput())

    drop_location = StringField('Drop Location', validators=[DataRequired()])
    drop_date = DateField('Drop date')
    # drop_time = SelectField('Drop time', choices=[('1-12', '01:00 - 12:00'), ('12-00', '12:00 - 00:00')])
    drop_contact_name = StringField('Full Name', validators=[Length(min=2, max=80)])
    drop_contact_phone = StringField('Phone Number', validators=[DataRequired(), Length(min=10)], widget=IntlTelInput())

    estimated_weight = IntegerField('Estimated Weight in tons', validators=[DataRequired()])
    truck_type = SelectField('Lorry type Needed', choices=[('open', 'Open'), ('close', 'Closed'), ('container', 'Container'), ('tanker', 'Tanker')], validators=[DataRequired()])
    material_details = TextAreaField('Material Details', validators=[DataRequired()])
    material_type = SelectField('Type of Materials', choices = [
    ('construction', 'Construction Materials'),
    ('agriculture', 'Agricultural Produce'),
    ('chemicals', 'Industrial Chemicals'),
    ('furniture', 'Furniture'),
    ('electronics', 'Electronics'),
    ('machinery', 'Heavy Machinery'),
    ('packaged', 'Packaged Goods'),
    ('liquid', 'Liquid Cargo'),
    ('perishables', 'Perishable Goods'),
    ('scrap', 'Metal Scrap'),
], validators=[DataRequired()])
    submit = SubmitField('Register the Material')