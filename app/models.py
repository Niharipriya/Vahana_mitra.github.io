from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, DateTime, ForeignKey, ARRAY, BLOB
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from flask_login import UserMixin

from app import db

class User(db.Model, UserMixin):
    __tablename__ = 'USER'

    user_id: Mapped[int] = mapped_column(primary_key=True)
    fullname: Mapped[str] = mapped_column(String, nullable=False)
    password_hash: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    email: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    phone: Mapped[str] = mapped_column(String, nullable=True, unique=True)

    creation_time: Mapped[datetime] = mapped_column(DateTime, default= datetime.utcnow)
    update_time: Mapped[datetime] = mapped_column(DateTime, default= datetime.utcnow, onupdate= datetime.utcnow)

    truck = db.relationship('Truck', backref='owner', lazy=True, cascade='all, delete-orphan')
    load = db.relationship('Load', backref='shipper', lazy=True, cascade='all, delete-orphan')

    def get_id(self):
        return str(self.user_id)

class Truck(db.Model):
    __tablename__ = 'TRUCK'

    truck_id: Mapped[int] = mapped_column(primary_key= True)
    user_id: Mapped[int] = mapped_column(ForeignKey('USER.user_id'), nullable=False)

    registration_number: Mapped[int] = mapped_column(String(10), unique=True)
    model_name: Mapped[str] = mapped_column(nullable= False)
    type: Mapped[str] = mapped_column(nullable= False)
    capacity: Mapped[float] = mapped_column(nullable= False)
    current_location: Mapped[str] = mapped_column(nullable= False)
    available_locations: Mapped[str] = mapped_column()

    owner_name: Mapped[str] = mapped_column(nullable= False)
    owner_phone: Mapped[str] = mapped_column(nullable= False)
    owner_aadhaar: Mapped[str] = mapped_column(nullable= False)
    owner_pan: Mapped[str] = mapped_column()

    driver_name: Mapped[str] = mapped_column()
    driver_aadhaar: Mapped[str] = mapped_column()
    driver_license: Mapped[str] = mapped_column()

    is_verified: Mapped[bool] = mapped_column(default= False)
    is_available: Mapped[bool] = mapped_column(default= True)
    tds: Mapped[str] = mapped_column()
    insurance: Mapped[str] = mapped_column()

    load: Mapped[set] = mapped_column(BLOB ,default= [])

    @classmethod
    def get_by_user(cls, user_id):
        """Get all trucks owned by a specific user

        Args:
            user_id (int): primary key for USER model
        """
        return cls.query.filter_by(user_id=user_id).all()

    @classmethod
    def find_available_trucks(cls, location=None, min_capacity=None, truck_type=None):
        query = cls.query.filter(cls.is_available == True, cls.is_verified == True)

        query = query.filter(cls.current_location.ilike(f"%{location}%")) if location else query
        query = query.filter(cls.type.ilike(f"%{truck_type}%")) if truck_type else query
        query = query.filter(cls.capacity >= min_capacity) if min_capacity else query
        return [truck.truck_id for truck in query.all()]

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

    @classmethod
    def load_truck(cls, load_id, truck_id):
        truck = cls.query.filter_by(truck_id=truck_id).first()

class Load(db.Model):
    __tablename__ = 'LOAD'

    load_id: Mapped[int] = mapped_column(primary_key= True)
    user_id: Mapped[int] = mapped_column(ForeignKey('USER.user_id'), unique= True, nullable= False)
    type: Mapped[str] = mapped_column(nullable= False)
    weight: Mapped[str] = mapped_column(nullable= False)
    details: Mapped[str] = mapped_column(nullable= False)

    pickup_contact_name: Mapped[str] = mapped_column()
    pickup_contact_phone: Mapped[str] = mapped_column()
    pickup_address: Mapped[str] = mapped_column()
    pickup_datetime: Mapped[datetime] = mapped_column()

    drop_contact_name: Mapped[str] = mapped_column()
    drop_contact_phone: Mapped[str] = mapped_column()
    drop_address: Mapped[str] = mapped_column()
    drop_datetime: Mapped[datetime] = mapped_column()

    cost: Mapped[float] = mapped_column()
    is_active: Mapped[bool] = mapped_column()
    in_progress: Mapped[bool] = mapped_column()
    truck: Mapped[int] = mapped_column()

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
    def find_available_loads(cls, capacity=None, current_location=None, ):

        query = cls.query.filter(cls.is_active == True, cls.in_progress == False)
        query = query.filter(cls.weight <= capacity) if capacity else query
        query = query.filter(cls.pickup_address.ilike(f"%{current_location}%")) if current_location else query
        return [load.load_id for load in query.all()]
        