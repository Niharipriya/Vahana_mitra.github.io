from flask import (
    Blueprint,
    session, 
    render_template
)

from app.constants.session_keys import SessionKeys
from app.form import LoadRegistrationForm, TruckRegistrationForm
from app.utils import autofill_fields

bp = Blueprint(
    'register',
    __name__,
    url_prefix='/register',
    template_folder= 'templates'
)

@bp.route('/truck/<int:id>', methods = ['POST', 'GET'])
def truck(id: int):
    form = TruckRegistrationForm( data = autofill_fields(
        'truck-',
        session[SessionKeys.PENDING_FORM_DATA],
        TruckRegistrationForm()
    ))

    return render_template(
       "truck_registration_form.html" ,
       form = form
    )

@bp.route('/load/<int:id>', methods = ['POST', 'GET'])
def load(id: int):
    form = LoadRegistrationForm(data = autofill_fields(
        'load-',
        session[SessionKeys.PENDING_FORM_DATA],
        LoadRegistrationForm()
    ))

    return render_template(
        "load_registration_form.html",
        form = form
    )