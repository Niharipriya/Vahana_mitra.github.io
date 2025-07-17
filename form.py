from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, TelField, SubmitField, PasswordField, BooleanField, DateField, SelectField, IntegerField, HiddenField
from wtforms.validators import DataRequired, Email, Length, EqualTo, Regexp

pickup_hour = SelectField(
    'Pickup Hour',
    choices=[(f"{h:02}", f"{h:02}") for h in range(0, 24)],
    validators=[DataRequired()]
)

pickup_minute = SelectField(
    'Pickup Minute',
    choices=[("00", "00"), ("30", "30")],
    validators=[DataRequired()]
)

pickup_time = HiddenField('Pickup Time', validators=[DataRequired()])

class SignupForm(FlaskForm):
    fullname = StringField('Full Name', validators=[DataRequired(), Length(min=2, max=80)])
    phone = TelField('Phone Number', validators=[DataRequired(), Length(min=10)])
    country_code = StringField('Country Code', validators=[DataRequired()]) # NEW
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

# class MaterialRegistrationForm(FlaskForm):
#     load_name = StringField('Owner of the Materials', validators=[DataRequired(), Length(min=8, max=80)])
#     pickup_address = StringField('Material Pick Up Address', validators=[DataRequired()])
#     drop_address = StringField('Material Drop off Address', validators=[DataRequired()])
#     submit = SubmitField('Add')

class TruckRegistrationForm(FlaskForm):
    truck_number = StringField('Registration number', validators=[DataRequired(), Length(min=9, max=10), Regexp(RTO_number_regex, message=("Invalid RTO number"))])
    truck_type = SelectField('Lorry type Needed', choices=[('open', 'Open'), ('close', 'Closed'), ('container', 'Container'), ('tanker', 'Tanker')], validators=[DataRequired()])
    capacity = IntegerField('Max load capacity in tons', validators=[DataRequired()])
    current_location = StringField('Current location from ', validators=[DataRequired()])
    destination_location = StringField('Preferred destination location')
    available_date = DateField('Date Available', validators=[DataRequired()])
    contact_number = TelField('Contact Number', validators=[DataRequired(), Length(min=10)])

class MaterialRegistrationForm(FlaskForm):
    pickup_location = StringField('Pickup Location', validators=[DataRequired()])
    pickup_date = DateField('Pickup date', validators=[DataRequired()])

    pickup_hour = SelectField(
        'Pickup Hour',
        choices=[(f"{h:02}", f"{h:02}") for h in range(0, 24)],
        validators=[DataRequired()]
    )

    pickup_minute = SelectField(
        'Pickup Minute',
        choices=[(f"{h:02}", f"{h:02}") for h in range(0, 60)],
        validators=[DataRequired()]
    )

    pickup_time = HiddenField('Pickup Time', validators=[DataRequired()])  # This will be filled with "HH:MM" from JS

    drop_location = StringField('Drop Location', validators=[DataRequired()])
    drop_date = DateField('Drop date', validators=[DataRequired()])
    drop_time = SelectField('Drop time', choices=[('1-12', '01:00 - 12:00'), ('12-00', '12:00 - 00:00')], validators=[DataRequired()])
    material_type = StringField('Type of Material', validators=[DataRequired()])
    estimated_weight = IntegerField('Estimated Weight in tons', validators=[DataRequired()])
    truck_type = SelectField('Lorry type Needed', choices=[('open', 'Open'), ('close', 'Closed'), ('container', 'Container'), ('tanker', 'Tanker')], validators=[DataRequired()])
    contact_number = TelField('Contact Number', validators=[DataRequired()])
    submit = SubmitField('Request Lorry')