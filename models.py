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
    user_id = db.Column(db.Integer, db.ForeignKey('USER.user_id'), nullable=False)

    truck_owner_name = db.Column(db.String(100), nullable=False)
    truck_RTO_number = db.Column(db.String(10), nullable=False, unique=True)
    truck_type = db.Column(db.String(80))
    capacity = db.Column(db.Float)
    current_location = db.Column(db.Text)
    is_verified = db.Column(db.Boolean, default=False)
    availability = db.Column(db.Boolean, default=True)

class Load(db.Model):
    __tablename__ = 'LOAD'

    load_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('USER.user_id'), unique=True)

    load_type = db.Column(db.String(100), nullable=False)
    load_details = db.Column(db.Text, nullable=False) 
    load_weight = db.Column(db.Float, nullable=False)
    pickup_address = db.Column(db.Text, nullable=False)
    pickup_contact = db.Column(db.Text, nullable=False)
    pickup_date = db.Column(db.DateTime, nullable=False)
    drop_address = db.Column(db.Text, nullable=False)
    drop_contact = db.Column(db.Text, nullable=False)
    drop_date = db.Column(db.DateTime, nullable=False)
    cost = db.Column(db.Float)
    is_active = db.Column(db.Boolean, default=True)
    in_progress = db.Column(db.Boolean, default=False)

class Booking(db.Model):
    __tablename__ = 'BOOKING'

    booking_id = db.Column(db.Integer, primary_key=True)
    truck_id = db.Column(db.Integer, db.ForeignKey('TRUCK.truck_id'), unique=True)
    load_id = db.Column(db.Integer, db.ForeignKey('LOAD.load_id'), unique=True)

    status = db.Column(db.String(50), default='Pending')

    truck = db.relationship('Truck', backref='booking', lazy=True)
    load = db.relationship('Load', backref='booking', lazy=True)