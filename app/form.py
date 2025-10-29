from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, TelField, SubmitField, PasswordField, BooleanField, DateField, SelectField, IntegerField
from wtforms import HiddenField, TextAreaField, DateTimeField, FileField
from wtforms.validators import DataRequired, Email, Length, EqualTo, Regexp, ValidationError, Optional

from app.constants.variable_constants import User_conts, Truck_conts, Load_conts
from app.models import User

"""
Make sure to make all the validation on the client side with wtforms validators
"""

class SignupForm(FlaskForm):
    user_fullname = StringField('Full Name', validators=[DataRequired(), Length(min=2, max=80)])
    user_phone = StringField('Phone Number', validators=[DataRequired(), Length(min=10)])
    user_email = EmailField('Email', validators=[DataRequired(), Email()])
    user_password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    submit = SubmitField('Signup')

    def validate_user_email(self, field):
        if User.find_by(User_conts.EMAIL, field.data):
            raise ValidationError(f"{field.data} is already registered")

    def validate_user_phone(self, field):
        if User.find_by(User_conts.PHONE, field.data):
            raise ValidationError(f"Already have an account with number {field.data}")

class LoginForm(FlaskForm):
    user_phone = StringField('Phone Number', validators=[Length(min=10), Optional()])
    user_email = EmailField('Email', validators=[Email(), Optional()])
    user_password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    submit = SubmitField('Login')

    # Ether phone or email should be provided
    def validate(self, extra_validators=None):
        if not super().validate():
            return False
        if not (getattr(self, User_conts.EMAIL).data or getattr(self, User_conts.PHONE).data):
            msg = "Either Email or Phone number is required to login"
            getattr(self, User_conts.EMAIL).errors.append(msg)
            getattr(self, User_conts.PHONE).errors.append(msg)
            return False
        return True

    def validate_user_email(self, field):
        if User.find_by(User_conts.EMAIL, field.data) is None:
            raise ValidationError("Invalid Email address")
    def validate_user_phone(self, field):
        # if User.find_by(User_conts.PHONE, field.data) is None:
        #     raise ValidationError("Invalid Username")
        """
        Normalize and validate the phone number before form submission.
        """
        # Remove any non-digit characters (like +, spaces, hyphens)
        digits = ''.join([c for c in field.data if c.isdigit()])
        field.data = digits  # Save cleaned version back into form data

        # Validate length — adjust to your country logic
        if len(digits) < 10:
            raise ValidationError('Phone number too short. Must have at least 10 digits.')
        elif len(digits) > 15:
            raise ValidationError('Phone number too long. Maximum allowed is 15 digits.')

class TruckRequestForm(FlaskForm):
    locals()[Load_conts.PICKUP_LOCATION] = StringField('Pickup Location', validators=[DataRequired()]) 
    locals()[Load_conts.DROP_LOCATION] = StringField('Drop Location', validators=[DataRequired()])
    locals()[Truck_conts.VEHICLE_TYPE] = SelectField('Lorry type Needed', choices= Truck_conts.VEHICLE_TYPE_CHOICES, validators=[DataRequired()])
    locals()[Load_conts.LOAD_WEIGHT] = IntegerField('Estimated Weight in tons', validators=[DataRequired()])
    submit = SubmitField('Request Lorry')

class TruckRegistrationForm(FlaskForm):
    truck_current_location = StringField('Current location from ', validators=[DataRequired()]) #Auto GPS detection in future
    vehicle_registration_number = StringField(
        'Registration number', 
        validators=[DataRequired(), Length(min=9, max=10)]
    )
    vehicle_model_name = StringField(
        'Trucks Model', 
        validators=[DataRequired()]
    )
    vehicle_type = SelectField('Lorry type Needed', choices=Truck_conts.VEHICLE_TYPE_CHOICES, validators=[DataRequired()])
    vehicle_capacity = IntegerField('Max load capacity in tons', validators=[DataRequired()])
    vehicle_insurance = FileField('Vehicle Insurance')
    vehicle_permit = StringField('Vehicle permits')

    truck_owner_name = StringField('Owners name', validators=[Length(min=10)])
    truck_owner_phone = StringField('Phone Number', validators=[Length(min=10, max=20)])
    truck_owner_aadhaar = StringField('Owners Aadhaar number', validators=[Regexp(Truck_conts.AADHAAR_REGEX, message="Write a valid aadhaar number")])
    truck_owner_pan = StringField('Owners PAN card number', validators=[Regexp(Truck_conts.PAN_REGEX, message="Enter a valid PAN number")])

    truck_driver_name = StringField('Driver Name')
    truck_driver_phone = StringField('Driver Phone number')
    truck_driver_aadhaar = StringField('Driver Aadhaar')
    truck_driver_license = FileField('Driver Driving License')

    available_date = DateField('Date Available')
    destionation_preference = StringField('Prefered destination location')
    request_load = SubmitField('Available for load requests')
    submit = SubmitField('Register Truck')

class LoadRequestForm(FlaskForm):
    locals()[Truck_conts.VEHICLE_TYPE] = SelectField('Lorry type Needed', choices=Truck_conts.VEHICLE_TYPE_CHOICES, validators=[DataRequired()])
    locals()[Truck_conts.VEHICLE_CAPACITY] = IntegerField('Max load capacity in tons', validators=[DataRequired()])
    locals()[Truck_conts.CURRENT_LOCATION] = StringField('Current location from ', validators=[DataRequired()])

    destination_location = StringField('Prefered destination location')
    submit = SubmitField('Request Lorry')

class LoadRegistrationForm(FlaskForm):
    pickup_location = StringField('Pickup Location', validators=[DataRequired()])
    pickup_datetime = DateField('Pickup date', validators=[DataRequired()])
    pickup_contact_name = StringField('Full Name', validators=[Length(min=2, max=80)])
    pickup_contact_phone = StringField('Phone Number', validators=[Length(min=10)])

    drop_location = StringField('Drop Location', validators=[DataRequired()])
    drop_datetime = DateField('Drop date')
    drop_contact_name = StringField('Full Name', validators=[Length(min=2, max=80)])
    drop_contact_phone = StringField('Phone Number', validators=[DataRequired(), Length(min=10)])

    load_weight = IntegerField('Estimated Weight in tons', validators=[DataRequired()])
    vehicle_type = SelectField('Lorry type Needed', choices=Truck_conts.VEHICLE_TYPE_CHOICES, validators=[DataRequired()])
    load_details = TextAreaField('Material Details', validators=[DataRequired()])
    load_type = SelectField('Type of Materials', choices=Load_conts.LOAD_TYPE_CHOICES, validators=[DataRequired()])

    request_truck = SubmitField('Request Lorry')
    submit = SubmitField('Register the Material')