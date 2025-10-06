from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, TelField, SubmitField, PasswordField, BooleanField, DateField, SelectField, IntegerField
from wtforms import HiddenField, TextAreaField, DateTimeField, FileField
from wtforms.validators import DataRequired, Email, Length, EqualTo, Regexp, ValidationError

from app.constants.variable_constants import User_conts, Truck_conts, Load_conts
from app.models import User

class SignupForm(FlaskForm):
    locals()[User_conts.FULLNAME] = StringField('Full Name', validators=[DataRequired(), Length(min=2, max=80)])
    locals()[User_conts.PHONE] = StringField('Phone Number', validators=[DataRequired(), Length(min=10, max=13)])
    locals()[User_conts.EMAIL] = EmailField('Email', validators=[DataRequired(), Email()])
    locals()[User_conts.PASSWORD] = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    submit = SubmitField('Signup')

    def validate_user_email(self, field):
        if User.find_by(User_conts.EMAIL, field.data):
            raise ValidationError(f"{field.data} is already registered")

    def validate_user_phone(self, field):
        if User.find_by(User_conts.PHONE, field.data):
            raise ValidationError(f"Already have an account with number {field.data}")

class LoginForm(FlaskForm):
    locals()[User_conts.PHONE] = StringField('Phone Number', validators=[DataRequired(), Length(min=10)])
    locals()[User_conts.EMAIL] = EmailField('Email', validators=[DataRequired(), Email()])
    locals()[User_conts.PASSWORD] = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    submit = SubmitField('Login')

    def validate_user_phone(self, field):
        if User.find_by(User_conts.PHONE, field.data) is None:
            raise ValidationError("Invalid Username")

class TruckRequestForm(FlaskForm):
    locals()[Load_conts.PICKUP_LOCATION] = StringField('Pickup Location', validators=[DataRequired()]) 
    locals()[Load_conts.DROP_LOCATION] = StringField('Drop Location', validators=[DataRequired()])
    locals()[Truck_conts.VEHICLE_TYPE] = SelectField('Lorry type Needed', choices= Truck_conts.VEHICLE_TYPE_CHOICES, validators=[DataRequired()])
    locals()[Load_conts.LOAD_WEIGHT] = IntegerField('Estimated Weight in tons', validators=[DataRequired()])
    submit = SubmitField('Request Lorry')

class TruckRegistrationForm(FlaskForm):
    locals()[Truck_conts.CURRENT_LOCATION] = StringField('Current location from ', validators=[DataRequired()])

    locals()[Truck_conts.VEHICLE_REGISTRATION_NUMBER] = StringField(
        'Registration number', 
        validators=[DataRequired(), Length(min=9, max=10), Regexp(Truck_conts.RTO_NUMBER_REGEX, message="Invalid RTO number")]
    )
    locals()[Truck_conts.VEHICLE_MODEL_NAME] = StringField(
        'Trucks Model', 
        validators=[DataRequired()]
    )
    locals()[Truck_conts.VEHICLE_TYPE] = SelectField('Lorry type Needed', choices=Truck_conts.VEHICLE_TYPE_CHOICES, validators=[DataRequired()])
    locals()[Truck_conts.VEHICLE_CAPACITY] = IntegerField('Max load capacity in tons', validators=[DataRequired()])
    locals()[Truck_conts.VEHICLE_INSURANCE] = FileField('Vehicle Insurance')
    locals()[Truck_conts.VEHICLE_PERMIT] = StringField('Vehicle permits')

    locals()[Truck_conts.OWNER_NAME] = StringField('Owners name', validators=[Length(min=10)])
    locals()[Truck_conts.OWNER_PHONE] = StringField('Phone Number', validators=[Length(min=10, max=20)])
    locals()[Truck_conts.OWNER_AADHAAR] = StringField('Owners Aadhaar number', validators=[Regexp(Truck_conts.AADHAAR_REGEX, message="Write a valid aadhaar number")])
    locals()[Truck_conts.OWNER_PAN] = StringField('Owners PAN card number', validators=[Regexp(Truck_conts.PAN_REGEX, message="Enter a valid PAN number")])

    locals()[Truck_conts.DRIVER_NAME] = StringField('Driver Name')
    locals()[Truck_conts.DRIVER_PHONE] = StringField('Driver Phone number')
    locals()[Truck_conts.DRIVER_AADHAAR] = StringField('Driver Aadhaar')
    locals()[Truck_conts.DRIVER_LICENSE] = FileField('Driver Driving License')

    available_date = DateField('Date Available')
    submit = SubmitField('Register Truck')

class LoadRequestForm(FlaskForm):
    locals()[Truck_conts.VEHICLE_TYPE] = SelectField('Lorry type Needed', choices=Truck_conts.VEHICLE_TYPE_CHOICES, validators=[DataRequired()])
    locals()[Truck_conts.VEHICLE_CAPACITY] = IntegerField('Max load capacity in tons', validators=[DataRequired()])
    locals()[Truck_conts.CURRENT_LOCATION] = StringField('Current location from ', validators=[DataRequired()])

    destination_location = StringField('Prefered destination location')
    submit = SubmitField('Request Lorry')

class LoadRegistrationForm(FlaskForm):
    locals()[Load_conts.PICKUP_LOCATION] = StringField('Pickup Location', validators=[DataRequired()])
    locals()[Load_conts.PICKUP_DATETIME] = DateField('Pickup date', validators=[DataRequired()])
    locals()[Load_conts.PICKUP_CONTACT_NAME] = StringField('Full Name', validators=[Length(min=2, max=80)])
    locals()[Load_conts.PICKUP_CONTACT_PHONE] = StringField('Phone Number', validators=[Length(min=10)])

    locals()[Load_conts.DROP_LOCATION] = StringField('Drop Location', validators=[DataRequired()])
    locals()[Load_conts.DROP_DATETIME] = DateField('Drop date')
    locals()[Load_conts.DROP_CONTACT_NAME] = StringField('Full Name', validators=[Length(min=2, max=80)])
    locals()[Load_conts.DROP_CONTACT_PHONE] = StringField('Phone Number', validators=[DataRequired(), Length(min=10)])

    locals()[Load_conts.LOAD_WEIGHT] = IntegerField('Estimated Weight in tons', validators=[DataRequired()])
    locals()[Truck_conts.VEHICLE_TYPE] = SelectField('Lorry type Needed', choices=Truck_conts.VEHICLE_TYPE_CHOICES, validators=[DataRequired()])
    locals()[Load_conts.LOAD_DETAILS] = TextAreaField('Material Details', validators=[DataRequired()])
    locals()[Load_conts.LOAD_TYPE] = SelectField('Type of Materials', choices = Load_conts.LOAD_TYPE_CHOICES, validators=[DataRequired()])
    submit = SubmitField('Register the Material')