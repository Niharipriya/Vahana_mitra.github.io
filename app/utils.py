from flask import (
    session,
    flash,
    redirect, url_for
)
from flask_login import current_user
from flask_wtf import FlaskForm

from app.constants.session_keys import SessionKeys

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
) -> FlaskForm: 
    autofill_fields = {
        name.removeprefix(prefix): data
        for name, data in pending_form_data.get('fields', {}).items()
        if name.removeprefix(prefix) in form._fields
    }
    return autofill_fields

def autofill_db_dict(
    input_data: dict,
    database_class
):
    valid_fields = {
        column.name
        for column in database_class.__table__.columns
    }
    
    filtered_data = {
        column_name: data
        for column_name, data in input_data.items()
        if column_name in valid_fields
    }

    print(valid_fields, filtered_data)
    
    return database_class(**filtered_data)
