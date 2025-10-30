from flask import (
    session,
    flash,
    redirect, url_for
)
from flask_login import current_user
from flask_wtf import FlaskForm
from sqlalchemy.orm import DeclarativeMeta

from typing import Any, Type

from app.constants.session_keys import SessionKeys
from app.models import User

def _redirect_save(form):
    session[SessionKeys.PENDING_FORM_DATA] = {
        'fields': {
            field.name: field.data
            for field in form
            if not('csrf_token' in field.name or 'submit' in field.name)
        }
    }
    if not current_user.is_authenticated:
        flash("Please Login or Sigup to continue your booking process", 'danger')
        return redirect(url_for('auth.signup'))
    return redirect(f'/booking/{session[SessionKeys.BOOKING_TYPE]}')

def autofill_fields(
    prefix: str,
    pending_form_data: dict,
    form: FlaskForm
) -> dict[str, Any]: 
    autofill = {
        name.removeprefix(prefix): data
        for name, data in pending_form_data.get('fields', {}).items()
        if name.removeprefix(prefix) in form._fields and data is not None
    }
    print(f"Data from field autofill fields:{autofill}")
    return autofill

def _autofill_db_dict(
    input_data: dict[str, Any],
    database_class: Type[DeclarativeMeta],
):
    """
    Create a model instance from a dict whose keys may be database column names
    (from constants like User_conts.FULLNAME) instead of Python attribute names.

    - Uses SQLAlchemy's mapper to resolve column.name → attribute.key.
    - If the model defines a property setter (e.g. password), that will be used.
    - Ignores unknown keys safely.
    """
    # mapping from db column names → python attribute names
    column_map = {
        col.name: attr 
        for attr, col in database_class.__mapper__.columns.items()
        }

    obj = database_class()
    for key, value in input_data.items():
        if key not in column_map:
            continue

        attr_name = column_map[key]

        # If model has a property setter (e.g. password), prefer that
        prop_candidate = attr_name.lstrip("_")
        descriptor = getattr(type(obj), prop_candidate, None)
        if isinstance(descriptor, property) and descriptor.fset is not None:
            setattr(obj, prop_candidate, value)
        else:
            setattr(obj, attr_name, value)

    return obj

def make_admin_user(admin_email, admin_password, db):
    """Create an admin user if not exists."""
    if admin_email and admin_password:
        admin_user = User.query.filter_by(email=admin_email).first()
        if not admin_user:
            admin_user = User(
                fullname= "Admin",
                email= admin_email,
                password= admin_password,
                is_admin=True
            )
            db.session.add(admin_user)
            db.session.commit()
            print(f"Admin user created with email: {admin_email}")
        else:
            print(f"Admin user already exists with email: {admin_email}")
    else:
        print("ADMIN_EMAIL environment variable not set. Cannot create admin user.")

# function to populate testing data
def make_testing_data(db):
    print("Populating testing data...")
    import json
    from .models import Truck, Load, User

    with open("./testing_data.json", 'r') as file:
        testing_data = json.load(file)

    truck_testing_data = testing_data["trucks"]
    load_testing_data = testing_data["loads"]

    def make_get_user(user_id: int):
        email = f"test_user{user_id}@example.com"
        # check by ID only
        user = User.query.filter_by(id=user_id).first()
        if user:
            print(f"user:{user_id} already exists (email: {user.email}).")
            return user
        else:
            user = User(
                id=user_id,
                fullname=f"Test User {user_id}",
                email=email,
                password=f"password@{user_id}",
                is_admin=False
            )
            db.session.add(user)
            db.session.flush()  # ensures ID assignment if autoincrement
            print(f"✅ Created user {user_id} ({email})")
            return user


    for truck_data in truck_testing_data:
        user = make_get_user(truck_data['user_id'])

        existing_truck = Truck.query.filter_by(
            user_id = user.id,
            vehicle_registration_number=truck_data['vehicle_registration_number']).first()
        if existing_truck:
            print(f"Truck with registration number {truck_data['vehicle_registration_number']} for user_id {user.id} already exists. Skipping.")
            continue
        else:
            print(f"Truck created with registration number {truck_data['vehicle_registration_number']} for user_id {user.id}.")
            truck = Truck(**truck_data)
            db.session.add(truck)

    for load_data in load_testing_data:
        user = make_get_user(load_data['user_id'])

        from datetime import datetime
        if 'pickup_datetime' in load_data and 'drop_datetime' in load_data:
            load_data['pickup_datetime'] = datetime.fromisoformat(load_data['pickup_datetime'])
            load_data['drop_datetime'] = datetime.fromisoformat(load_data['drop_datetime'])

        existing_load = Load.query.filter_by(
            user_id= user.id,
            pickup_contact_name=load_data['pickup_contact_name']).first()
        if existing_load:
            print(f"Load with pickup contact name {load_data['pickup_contact_name']} for user_id {load_data['user_id']} already exists. Skipping.")
            continue
        else:
            print(f"Load created with pickup contact name {load_data['pickup_contact_name']} for user_id {load_data['user_id']}.")
            load = Load(**load_data)
            db.session.add(load)

    db.session.commit()
    print("Finished populating testing data.")