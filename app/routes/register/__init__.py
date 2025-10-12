from flask import (
    Blueprint, session, render_template,
    request, flash, redirect, url_for
)
from flask_login import current_user, login_required
from app.constants.session_keys import SessionKeys
from app.form import LoadRegistrationForm, TruckRegistrationForm
from app.utils import autofill_fields, _autofill_db_dict
from app.constants.variable_constants import User_conts, Load_conts, Truck_conts
from app.models import Load, Truck
from app import db


bp = Blueprint(
    'register',
    __name__,
    url_prefix='/register',
    template_folder='templates'
)


def _handle_form_submission(
    form, 
    model_cls, 
    success_message: str, 
    redirect_url: str, 
    extra_data: dict | None = None
):
    """
    Generic helper to handle validated form submissions for Truck and Load registrations.
    """
    try:
        # Combine form data and any additional fields
        form_data = {**form.data, **(extra_data or {})}
        form_data[User_conts.ID] = current_user.id

        # Convert to model instance
        instance = _autofill_db_dict(form_data, model_cls)
        db.session.add(instance)
        db.session.commit()

        flash(success_message, "success")
        session.clear()
        return redirect(redirect_url)

    except Exception as e:
        db.session.rollback()
        flash("An error occurred while saving your data. Please try again.", "danger")
        print(f"[ERROR] Failed to submit {model_cls.__name__}: {e}")
        return redirect(request.url)


@bp.route('/truck', methods=['GET', 'POST'])
@login_required
def truck():
    # Ensure session contains pending data
    pending_data = session.get(SessionKeys.PENDING_FORM_DATA, {})
    form = TruckRegistrationForm(
        data = autofill_fields('truck-', pending_data, TruckRegistrationForm())
    )

    if form.validate_on_submit():
        success_message = (
            f"Successfully registered your vehicle "
            f"{form.data.get(Truck_conts.VEHICLE_MODEL_NAME, '').title()}"
        )
        return _handle_form_submission(
            form,
            Truck,
            success_message,
            url_for('dashboard.index')
        )

    elif request.method == 'POST':
        flash("You have filled the form incorrectly. Please recheck the fields.", 'danger')
        print("[FORM ERRORS - TRUCK]", form.errors)

    return render_template(
        "truck_registration_form.html",
        form=form
    )


@bp.route('/load', methods=['GET', 'POST'])
@login_required
def load():
    pending_data = session.get(SessionKeys.PENDING_FORM_DATA, {})
    form = LoadRegistrationForm(
        data=autofill_fields('load-', pending_data, LoadRegistrationForm())
    )

    if form.validate_on_submit():
        form_data = form.data
        extra_data = {
            Load_conts.CURRENT_LOCATION: getattr(form, Load_conts.PICKUP_LOCATION).data
        }

        success_message = (
            f"Successfully scheduled a booking from "
            f"{form_data.get(Load_conts.PICKUP_LOCATION)} "
            f"to {form_data.get(Load_conts.DROP_LOCATION)}"
        )
        return _handle_form_submission(
            form,
            Load,
            success_message,
            url_for('dashboard.index'),
            extra_data
        )

    elif request.method == 'POST':
        flash("You have filled the form incorrectly. Please recheck the fields.", 'danger')
        print("[FORM ERRORS - LOAD]", form.errors)

    return render_template(
        "load_registration_form.html",
        form=form,
        current_user_fullname=current_user.fullname,
        current_user_phone=current_user.phone
    )
