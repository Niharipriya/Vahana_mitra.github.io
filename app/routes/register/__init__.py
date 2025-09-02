from flask import (
    Blueprint,
    session, 
    render_template, request
)
from flask_login import current_user

from app.constants.session_keys import SessionKeys
from app.form import LoadRegistrationForm, TruckRegistrationForm
from app.utils import autofill_fields, autofill_db_dict
from app.constants.variable_constants import User_conts, Load_conts
from app.models import Load, Truck, User
from app import db

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

    if form.validate_on_submit():
        print("adding truck")
        form_data  = form.data
        form_data[User_conts.ID] = getattr(
            current_user, 
            User.attribute_map(current_user)[User_conts.ID]
        )
        truck = autofill_db_dict(
            form_data,
            Truck
        )
        db.session.add(truck)
        db.session.commit()
    else:
        print("not a valid form")
        print(form.errors)
    
    if request.method == 'POST':
        print(form.errors)

    print("conformation")
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

    if form.validate_on_submit():
        print("adding load")
        form_data  = form.data
        form_data[User_conts.ID] = getattr(
            current_user, 
            User.attribute_map(current_user)[User_conts.ID]
        )
        form_data[Load_conts.CURRENT_LOCATION] = getattr(
            form,
            Load_conts.PICKUP_LOCATION
        ).data
        print(form_data)
        load = autofill_db_dict(
            form_data,
            Load
        )
        db.session.add(load)
        db.session.commit()
    else:
        print("not a valid form")
        print(form.errors)

    if request == 'POST':
        print(form.errors)
    
    print("conformation")

    return render_template(
        "load_registration_form.html",
        form = form,
        current_user_fullname = getattr(current_user, User.attribute_map(current_user)[User_conts.FULLNAME]),
        current_user_phone = getattr(current_user, User.attribute_map(current_user)[User_conts.PHONE])
    )