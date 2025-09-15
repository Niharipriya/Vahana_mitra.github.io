from flask import (
    session,
    flash,
    redirect, url_for
)
from flask_login import current_user
from flask_wtf import FlaskForm
from sqlalchemy.orm import DeclarativeMeta

from typing import Any, Type
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

def _autofill_db_dict(
    input_data: dict[str, Any],
    database_class: Type[DeclarativeMeta],
):
    """
    Create a model instance from a dict whose keys may be database column names
    (from constants like User_conts.FULLNAME) instead of Python attribute names.

    - Uses SQLAlchemy's mapper to resolve column.name → attribute.key.
    - If the model defines a property setter (e.g. password), that will be used.
    - Ignores unknown keys safely.
    """
    # mapping from db column names → python attribute names
    column_map = {
        col.name: attr 
        for attr, col in database_class.__mapper__.columns.items()
        }

    obj = database_class()
    for key, value in input_data.items():
        if key not in column_map:
            continue

        attr_name = column_map[key]

        # If model has a property setter (e.g. password), prefer that
        prop_candidate = attr_name.lstrip("_")
        descriptor = getattr(type(obj), prop_candidate, None)
        if isinstance(descriptor, property) and descriptor.fset is not None:
            setattr(obj, prop_candidate, value)
        else:
            setattr(obj, attr_name, value)

    return obj
