from uuid import uuid4
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, DateTime, ForeignKey, Float, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from typing import Optional, TypeVar, Type

from app import db
from app.constants.variable_constants import User_conts, Truck_conts, Load_conts

T = TypeVar("T", bound="ModelMixin")

class ModelMixin:
    @classmethod
    def _resolve_column(cls, field: str):
        """Safely resolve a column from a field string/constant."""
        # 1. Direct Python attribute (safe if used)
        if hasattr(cls, field):
            return getattr(cls, field)

        # 2. DB column name (constant → column.key)
        for attr, col in cls.__mapper__.columns.items():
            if col.name == field:
                return getattr(cls, attr)

        raise ValueError(f"Invalid field: {field} for model {cls.__name__}")

    @classmethod
    def find_by(cls: Type[T], field: str, value) -> Optional[T]:
        """Find a single record by one field (supports constants)."""
        return db.session.scalar(
            db.select(cls).where(cls._resolve_column(field) == value)
        )

    @classmethod
    def filter_by_fields(cls: Type[T], **kwargs) -> list[T]:
        """
        Filter by multiple fields.
        Example:
        User.filter_by_fields(email="x", phone="y")
        User.filter_by_fields(**{User_conts.EMAIL: "x"})
        """
        query = db.select(cls)
        for field, value in kwargs.items():
            query = query.where(cls._resolve_column(field) == value)
        return db.session.execute(query).scalars().all()

class User(db.Model, UserMixin, ModelMixin):
    __tablename__ = 'USER'

    id: Mapped[int] = mapped_column(primary_key=True, name=User_conts.ID)
    fullname: Mapped[str] = mapped_column(nullable=False, name=User_conts.FULLNAME)
    _password: Mapped[str] = mapped_column(nullable=False, unique=True, name=User_conts.PASSWORD)
    email: Mapped[str] = mapped_column(nullable=False, unique=True, index= True, name=User_conts.EMAIL)
    phone: Mapped[str] = mapped_column(nullable=True, unique=True, index= True, name=User_conts.PHONE)

    # Audit fields
    creation_time: Mapped[datetime] = mapped_column(default=datetime.utcnow, name=User_conts.CREATED_TIME)
    update_time: Mapped[datetime] = mapped_column(default=datetime.utcnow, onupdate=datetime.utcnow, name=User_conts.UPDATED_TIME)

    # Relationships
    truck = relationship('Truck', backref='owner', lazy=True, cascade='all, delete-orphan')
    load = relationship('Load', backref='shipper', lazy=True, cascade='all, delete-orphan')

    alternative_id: Mapped[str] = mapped_column(String, default=uuid4().hex, index= True)
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False, server_default='false')

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, password: str) -> None:
        if not password:
            return
        if self._password is None or not self.check_password(password):
            self._password = generate_password_hash(
                password,
                method="pbkdf2:sha256",
            )
            self.alternative_id = uuid4().hex

    def check_password(self, password: Optional["User"]):
        return bool(password) and check_password_hash(self._password, password)

class Truck(db.Model, ModelMixin):
    __tablename__ = 'TRUCK'

    truck_id: Mapped[int] = mapped_column(primary_key=True, name=Truck_conts.ID )
    user_id: Mapped[int] = mapped_column(ForeignKey(f"USER.{User_conts.ID}"), nullable=False )

    # Vehicle information
    vehicle_registration_number: Mapped[str] = mapped_column(String, unique=True, nullable=False, name=Truck_conts.VEHICLE_REGISTRATION_NUMBER)
    vehicle_model_name: Mapped[str] = mapped_column(String, nullable=False, name=Truck_conts.VEHICLE_MODEL_NAME)
    vehicle_type: Mapped[str] = mapped_column(String, nullable=False, name=Truck_conts.VEHICLE_TYPE)
    vehicle_capacity: Mapped[float] = mapped_column(Float, nullable=False, name=Truck_conts.VEHICLE_CAPACITY)
    vehicle_insurance: Mapped[str] = mapped_column(String, nullable=True, name=Truck_conts.VEHICLE_INSURANCE)
    current_location: Mapped[str] = mapped_column(String, nullable=False, name=Truck_conts.CURRENT_LOCATION)

    # Owner details
    owner_name: Mapped[str] = mapped_column(String, nullable=False, name=Truck_conts.OWNER_NAME)
    owner_phone: Mapped[str] = mapped_column(String, nullable=False, name=Truck_conts.OWNER_PHONE)
    owner_aadhaar: Mapped[str] = mapped_column(String, nullable=False, name=Truck_conts.OWNER_AADHAAR)
    owner_pan: Mapped[str] = mapped_column(String, nullable=True, name=Truck_conts.OWNER_PAN)

    # Driver details
    driver_name: Mapped[str] = mapped_column(String, nullable=True, name=Truck_conts.DRIVER_NAME)
    driver_phone: Mapped[str] = mapped_column(String, nullable=True, name=Truck_conts.DRIVER_PHONE)
    driver_aadhaar: Mapped[str] = mapped_column(String, nullable=True, name=Truck_conts.DRIVER_AADHAAR)
    driver_license: Mapped[str] = mapped_column(String, nullable=True, name=Truck_conts.DRIVER_LICENSE)

    # Status and documents
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    is_available: Mapped[bool] = mapped_column(Boolean, default=True)
    tds: Mapped[str] = mapped_column(String, nullable=True)

    # Relationships
    load = relationship('Load', backref='truck', lazy=True, cascade='all, delete-orphan')

    @classmethod
    def find_available_trucks(cls, location=None, min_capacity=None, truck_type=None):
        query = cls.query.filter(cls.is_available == True, cls.is_verified == True)

        if location:
            query = query.filter(cls.current_location.ilike(f"%{location}%"))
        if truck_type:
            query = query.filter(cls.vehicle_type.ilike(f"%{truck_type}%"))
        if min_capacity:
            query = query.filter(cls.vehicle_capacity >= min_capacity)

        return [truck.truck_id for truck in query.all()]

class Load(db.Model, ModelMixin):
    __tablename__ = 'LOAD'

    load_id: Mapped[int] = mapped_column(primary_key=True, name=Load_conts.ID)
    user_id: Mapped[int] = mapped_column(ForeignKey(f'USER.{User_conts.ID}'), nullable=False)
    truck_id: Mapped[int] = mapped_column(ForeignKey(f'TRUCK.{Truck_conts.ID}'), nullable=True)

    # Pickup details
    pickup_location: Mapped[str] = mapped_column(String, nullable=False, name=Load_conts.PICKUP_LOCATION)
    pickup_datetime: Mapped[datetime] = mapped_column(DateTime, nullable=False, name=Load_conts.PICKUP_DATETIME)
    pickup_contact_name: Mapped[str] = mapped_column(String, nullable=False, name=Load_conts.PICKUP_CONTACT_NAME)
    pickup_contact_phone: Mapped[str] = mapped_column(String, nullable=False, name=Load_conts.PICKUP_CONTACT_PHONE)

    # Drop details
    drop_location: Mapped[str] = mapped_column(String, nullable=False, name=Load_conts.DROP_LOCATION)
    drop_datetime: Mapped[datetime] = mapped_column(DateTime, nullable=False, name=Load_conts.DROP_DATETIME)
    drop_contact_name: Mapped[str] = mapped_column(String, nullable=False, name=Load_conts.DROP_CONTACT_NAME)
    drop_contact_phone: Mapped[str] = mapped_column(String, nullable=False, name=Load_conts.DROP_CONTACT_PHONE)

    # Cargo details
    load_type: Mapped[str] = mapped_column(String, nullable=False, name=Load_conts.LOAD_TYPE)
    load_weight: Mapped[float] = mapped_column(Float, nullable=False, name=Load_conts.LOAD_WEIGHT)
    load_details: Mapped[str] = mapped_column(String, nullable=True, name=Load_conts.LOAD_DETAILS)
    load_current_location: Mapped[str] = mapped_column(String, nullable=False, name=Load_conts.CURRENT_LOCATION)

    # Status and cost
    cost: Mapped[float] = mapped_column(Float, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    in_progress: Mapped[bool] = mapped_column(Boolean, default=False)

    @classmethod
    def find_available_loads(cls, capacity=None, current_location=None):
        query = cls.query.filter(cls.is_active == True, cls.in_progress == False)

        if capacity:
            query = query.filter(cls.load_weight <= capacity)
        if current_location:
            query = query.filter(cls.pickup_location.ilike(f"%{current_location}%"))

        return [load.load_id for load in query.all()]
