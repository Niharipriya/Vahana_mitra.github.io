from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin
from flask_bcrypt import Bcrypt

db = SQLAlchemy()

class User(db.Model, UserMixin):
    __tablename__ = 'USER'

    user_id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(80), nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=True)
    phone = db.Column(db.String(20), unique=True, nullable=True)

    creation_time = db.Column(db.DateTime, default=datetime.utcnow)
    update_time = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    truck = db.relationship('Truck', backref='owner', lazy=True, cascade='all, delete-orphan')
    load = db.relationship('Load', backref='shipper', lazy=True, cascade='all, delete-orphan')

    def get_id(self):
        return str(self.user_id)

    def check_password(self, password, bcrypt: Bcrypt):
        return bcrypt.check_password_hash(self.password_hash, password)

class Truck(db.Model):
    __tablename__ = 'TRUCK'

    truck_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('USER.user_id'), unique=True)

    ''' Can also add the following data/ Can also given to call center to handle the process 
        Truck Details
        truck_number, truck_type, brand, model, year, capacity_kg 

        Location and availability
        current_location, current_city, current_state

        Documents and verification
        registration_certificate, insurance_document, driver_license, truck_images

        Status and ratings
        is_verified average_rating total_trips
    '''
    truck_details = db.Column(db.Text, nullable=False)           #Keeping simple for demo
    availability = db.Column(db.Boolean, default=True)

class Load(db.Model):
    __tablename__ = 'LOAD'

    load_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('USER.user_id'), unique=True)

    ''' Can also add the following data/ Can also given to call center to handle the process 
        Weight and dimensions
        weight_kg length_meters width_meters height_meters quantity
        
        # Pickup Details
        pickup_address pickup_city pickup_state pickup_pincode pickup_contact_person pickup_contact_phone
        preferred_pickup_date pickup_time_flexibility 
        
        # Drop Details
        drop_address drop_city drop_state drop_pincode drop_contact_person = db.Column(db.String(100))
        drop_contact_phone preferred_delivery_date 

        # Pricing and payment
        budget_min budget_max payment_terms  # 'advance', 'on_delivery', 'net_30'
        
        load_images special_instructions is_active is_urgent = db.Column(db.Boolean, default=False)
        estimated_distance_km 
    '''
    load_details = db.Column(db.Text, nullable=False)           #Keeping simple for demo
    pickup_address = db.Column(db.Text, nullable=False)
    drop_address = db.Column(db.Text, nullable=False)

class Booking(db.Model):
    __tablename__ = 'BOOKING'

    booking_id = db.Column(db.Integer, primary_key=True)
    truck_id = db.Column(db.Integer, db.ForeignKey('TRUCK.truck_id'), unique=True)
    load_id = db.Column(db.Integer, db.ForeignKey('LOAD.load_id'), unique=True)

    status = db.Column(db.String(50), default='Pending')

    truck = db.relationship('Truck', backref='booking', lazy=True)
    load = db.relationship('Load', backref='booking', lazy=True)