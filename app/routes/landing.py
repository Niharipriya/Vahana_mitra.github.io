from flask import (
    Blueprint,
    render_template,
    flash, 
    session,
    redirect, url_for, request
)
from flask_login import current_user

from app.models import Truck, Load
from app.constants.session_keys import SessionKeys
from app.constants.variable_constants import Truck_conts, Load_conts
from app.form import TruckRequestForm, LoadRequestForm
from app.utils import _redirect_save

bp = Blueprint("landing", __name__, url_prefix="")

@bp.route("/", methods=['POST', 'GET'])
def index():
    truck_request_form = TruckRequestForm(prefix= 'load')
    load_request_form = LoadRequestForm(prefix= 'truck')

    if truck_request_form.validate_on_submit():
        session[SessionKeys.PENDING_FORM_DATA] = None
        session[SessionKeys.BOOKING_TYPE] = Load.__name__
        location= getattr(truck_request_form, Load_conts.PICKUP_LOCATION).data
        min_capacity= getattr(truck_request_form, Load_conts.LOAD_WEIGHT).data 
        truck_type= getattr(truck_request_form, Truck_conts.VEHICLE_TYPE).data
        print(f"Location: {location}, Min Capacity: {min_capacity}, Truck Type: {truck_type}")
        session[SessionKeys.COMPATIBLE_TRUCK_IDS] = Truck.find_available_trucks(location, min_capacity, truck_type)
        print("Compatible List for Trucks",session[SessionKeys.COMPATIBLE_TRUCK_IDS])
        return _redirect_save(truck_request_form)
    
    if load_request_form.validate_on_submit():
        session[SessionKeys.PENDING_FORM_DATA] = None
        session[SessionKeys.BOOKING_TYPE] = Truck.__name__
        session[SessionKeys.COMPATIBLE_LOAD_IDS] = Load.find_available_loads(
            capacity= getattr(load_request_form, Truck_conts.VEHICLE_CAPACITY).data,
            current_location= getattr(load_request_form, Truck_conts.CURRENT_LOCATION).data,
        )
        print("Compatible List for Load",session[SessionKeys.COMPATIBLE_LOAD_IDS])
        return _redirect_save(load_request_form)

    if request.method == "POST":
        print(f"Form errors: {truck_request_form.errors} {load_request_form.errors}")

    return render_template(
        'landing.html',
        truck_request_form = truck_request_form,
        load_request_form = load_request_form
    )