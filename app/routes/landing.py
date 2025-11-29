from flask import (
    Blueprint,
    render_template,
    session,
    request,
)

from app.models import Truck, Load
from app.constants.session_keys import SessionKeys
from app.form import TruckRegistrationForm, LoadRegistrationForm
from app.utils import _redirect_save, make_admin_user, make_testing_data

bp = Blueprint("landing", __name__, url_prefix="")


@bp.route("/", methods=["POST", "GET"])
def index():
    truck_form = TruckRegistrationForm()
    session[SessionKeys.TRUCK_CURRENT_LOCATION] = ""
    load_form = LoadRegistrationForm()
    session[SessionKeys.LOAD_PICKUP_LOCATION] = ""

    # if truck_form.request_load.data:
    #     session[SessionKeys.IN_PROGRESS] = True
    #     session[SessionKeys.BOOKING_TYPE] = (
    #         Truck.__name__
    #     )  # User is booking a load for there truck, i.e. entering there truck details
    #     session[SessionKeys.TRUCK_CURRENT_LOCATION] = (
    #         truck_form.truck_current_location.data
    #     )
    #
    #     return _redirect_save(truck_form)

    if load_form.request_truck.data:
        session[SessionKeys.IN_PROGRESS] = True
        session[SessionKeys.BOOKING_TYPE] = (
            Load.__name__
        )  # User is Booking a Truck for there load, ie entering there load details
        session[SessionKeys.LOAD_PICKUP_LOCATION] = load_form.pickup_location.data

        return _redirect_save(
            load_form, f"/booking/{session[SessionKeys.BOOKING_TYPE]}"
        )

    if request.method == "POST":
        print(f"Form errors: {truck_form.errors} {load_form.errors}")

    return render_template("landing.html", truck_form=truck_form, load_form=load_form)


@bp.route("/testing_landingV2")
def indexV2():
    return render_template("landing_v3.html")
