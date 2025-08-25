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
      list_compatible = session[SessionKeys.COMPATIBLE_LOAD_IDS] if booking_type == 'Load' else session[SessionKeys.COMPATIBLE_TRUCK_IDS]
      
      return render_template(
            'booking.html',
            booking_type = booking_type,
            list_compatible = list_compatible 
      )