from flask import (
    Blueprint, 
    render_template, 
    session
)
from flask_login import login_required

from app.constants.session_keys import SessionKeys
from app.models import Load, Truck

bp = Blueprint(
    'booking', 
    __name__, 
    url_prefix='/booking',
    template_folder= 'templates'
)

@bp.route('/<string:booking_type>')
@login_required
def booking(booking_type: str):
    list_compatible_loads = []
    list_compatible_trucks = []

    # User is booking there load find comatible trucks for there load
    if booking_type == 'Load' and session.get(SessionKeys.LOAD_PICKUP_LOCATION):
        load_pickup_location = session.get(SessionKeys.LOAD_PICKUP_LOCATION)
        list_compatible_trucks = Truck.find_available_trucks(location= load_pickup_location)

        print(f'''
            Booking Type: {session[SessionKeys.BOOKING_TYPE]},
            Truck Current Loaction: {session[SessionKeys.LOAD_PICKUP_LOCATION]},
            List of Compatible Trucks: {list_compatible_trucks}
        ''')
    elif booking_type == 'Truck' and session.get(SessionKeys.TRUCK_CURRENT_LOCATION):
        truck_current_location = session.get(SessionKeys.TRUCK_CURRENT_LOCATION)
        list_compatible_loads = Load.find_available_loads(current_location= truck_current_location)

        print(f'''
            Booking Type: {session[SessionKeys.BOOKING_TYPE]},
            Load Pickup Location: {session[SessionKeys.TRUCK_CURRENT_LOCATION]},
            List of Compatible Trucks: {list_compatible_loads}
        ''')
    return render_template(
        'booking.html',
        booking_type=booking_type,
        list_compatible_loads=list_compatible_loads,
        list_compatible_trucks=list_compatible_trucks
    )