from flask import (
      Blueprint, 
      render_template, 
      session
)

from app.constants.session_keys import SessionKeys

bp = Blueprint(
      'booking', 
      __name__, 
      url_prefix='/booking',
      template_folder= 'templates'
)

@bp.route('/<string:booking_type>')
def booking(booking_type: str):
      list_compatible = []
      if booking_type == 'Load' and session.get(SessionKeys.COMPATIBLE_LOAD_IDS):
            list_compatible = session.get(SessionKeys.COMPATIBLE_LOAD_IDS)
      elif booking_type == 'Truck' and session.get(SessionKeys.COMPATIBLE_TRUCK_IDS):
            list_compatible = session.get(SessionKeys.COMPATIBLE_TRUCK_IDS)
      
      return render_template(
            'booking.html',
            booking_type = booking_type,
            list_compatible = list_compatible 
      )