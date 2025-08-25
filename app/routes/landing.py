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
        session[SessionKeys.COMPATIBLE_TRUCK_IDS] = Truck.find_available_trucks(
            location= truck_request_form.pickup_location.data,
            min_capacity= truck_request_form.estimated_weight.data, 
            truck_type= truck_request_form.truck_type.data
        )
        return _redirect_save(truck_request_form)
    
    if load_request_form.validate_on_submit():
        session[SessionKeys.PENDING_FORM_DATA] = None
        session[SessionKeys.BOOKING_TYPE] = Truck.__name__
        session[SessionKeys.COMPATIBLE_LOAD_IDS] = Load.find_available_loads(
            capacity= load_request_form.capacity.data,
            current_location= load_request_form.current_location.data,
        )
        return _redirect_save(load_request_form)

    if request.method == "POST":
        print(f"Form errors: {truck_request_form.errors} {load_request_form.errors}")

    return render_template(
        'landing.html',
        truck_request_form = truck_request_form,
        load_request_form = load_request_form
    )