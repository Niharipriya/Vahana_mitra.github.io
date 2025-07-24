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
    user_id = db.Column(db.Integer, db.ForeignKey('USER.user_id'), unique=True, nullable=False)
    # load_id = db.Column(db.Integer, db.ForeignKey('LOAD.load_id'), unique=True, nullable=True)

    registration_number = db.Column(db.String(10), nullable=False, unique=True)
    model_name = db.Column(db.Text, nullable=False)
    type = db.Column(db.String(80), nullable=False)
    capacity = db.Column(db.Float, nullable=False)
    current_location = db.Column(db.Text, nullable=False)
    available_locations = db.Column(db.Text)

    owner_name = db.Column(db.String(100), nullable=False)
    owner_aadhaar = db.Column(db.String(12))
    owner_mobile = db.Column(db.Integer)
    owner_tos = db.Column(db.Text)
    owner_pan = db.Column(db.String(10))

    is_verified = db.Column(db.Boolean, default=False)
    is_available = db.Column(db.Boolean, default=True)
    availability = db.Column(db.Integer)

    @classmethod
    def get_by_user(cls, user_id):
        """Get all trucks owned by a specific user

        Args:
            user_id (int): primary key for USER model
        """
        return cls.query.filter_by(user_id=user_id).all()

    @classmethod
    def find_available_truck(cls, location=None, min_capacity=None, truck_type=None):
        query = cls.query.filter(cls.is_available == True, cls.is_verified == True)

        query = query.filter(cls.current_location.ilike(f"%{location}%")) if location else query
        query = query.filter(cls.type.ilike(f"%{truck_type}%")) if truck_type else query
        query = query.filter(cls.capacity >= min_capacity) if min_capacity else query
        return query.all()

    @classmethod
    def from_json(cls, data):
        """Adds a new User from JSON test data."""
        if not cls.get_by_user(data['user_id']):
            user = cls(**data)
            db.session.add(user)
            db.session.commit()

    @classmethod
    def delete_by_json(cls, data):
        """Deletes a user by matching a unique field (like email) from JSON."""
        user = cls.get_by_user(data['user_id'])
        if user:
            db.session.delete(user)
            db.session.commit()

class Load(db.Model):
    __tablename__ = 'LOAD'

    load_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('USER.user_id'), unique=True, nullable=False)
    # truck_id = db.Column(db.Integer, db.ForeignKey('TRUCK.truck_id'), unique=True, nullable=True)
    type = db.Column(db.String(100), nullable=False)
    details = db.Column(db.Text, nullable=False) 
    weight = db.Column(db.Float, nullable=False)

    pickup_address = db.Column(db.Text, nullable=False)
    pickup_contact_name = db.Column(db.String(100))
    pickup_contact_phone = db.Column(db.Integer, nullable=False)
    pickup_date = db.Column(db.DateTime, nullable=False)                            #loading date

    drop_address = db.Column(db.Text, nullable=False)
    drop_contact_name = db.Column(db.Integer)
    drop_contact_phone = db.Column(db.String(100), nullable=False)
    drop_date = db.Column(db.DateTime, nullable=False)                              #auto calculate from the pickup to drop

    cost = db.Column(db.Float)
    load_image = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=True)
    in_progress = db.Column(db.Boolean, default=False)

    @classmethod
    def get_by_user(cls, user_id):
        """Get all trucks owned by a specific user

        Args:
            user_id (int): primary key for USER model
        """
        return cls.query.filter_by(user_id=user_id).all()

    @classmethod
    def from_json(cls, data):
        """Adds a new User from JSON test data."""
        if not cls.get_by_user(data['user_id']):

            pickup_date = datetime.fromisoformat(data['pickup_date'])
            drop_date = datetime.fromisoformat(data['drop_date'])

            user = cls(
                user_id=data.get('user_id'),
                type=data.get('type'),
                details=data.get('details'),
                weight=data.get('weight'),
                pickup_address=data.get('pickup_address'),
                pickup_contact_name=data.get('pickup_contact_name'),
                pickup_contact_phone=data.get('pickup_contact_phone'),
                pickup_date=pickup_date,
                drop_address=data.get('drop_address'),
                drop_contact_name=data.get('drop_contact_name'),
                drop_contact_phone=data.get('drop_contact_phone'),
                drop_date=drop_date,
                cost=data.get('cost'),
                load_image=data.get('load_image'),
                is_active=data.get('is_active', True),
                in_progress=data.get('in_progress', False)
            )
            db.session.add(user)
            db.session.commit()

    @classmethod
    def delete_by_json(cls, data):
        """Deletes a user by matching a unique field (like email) from JSON."""
        user = cls.get_by_user(data['user_id'])
        if user:
            db.session.delete(user)
            db.session.commit()

    @classmethod
    def find_available_materials(cls, capacity=None, current_location=None, ):

        query = cls.query.filter(cls.is_active == True, cls.in_progress == False)
        query = query.filter(cls.weight <= capacity) if capacity else query
        query = query.filter(cls.pickup_address.ilike(f"%{current_location}%")) if current_location else query
        return query.all()
        