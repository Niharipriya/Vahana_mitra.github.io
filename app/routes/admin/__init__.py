from flask_login import current_user
from flask import flash, redirect, url_for
from flask_admin import AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView
from wtforms import PasswordField,SelectField

from app import admin
from app.models import User, Truck, Load

class AdminView(AdminIndexView):
    """Generic admin view with access control.

    Methods:
    -------:
        is_accessible: Check if the current user is an admin.
        inaccessible_callback: Redirect to login page if the user doesn't have access.
    """
    def is_accessible(self):
        """Check if the current user is an admin."""
        return current_user.is_authenticated and current_user.is_admin

    def inaccessible_callback(self, name, **kwargs):
        """Handle the response to inaccessible views by aborting with 403."""
        flash("You do not have permission to access the admin panel.", "danger")
        from flask import abort
        return abort(403)

class UserAdminView(ModelView):
    """Admin view for the User model with customizations.

    Columns:
    --------:
        id: User ID
        fullname: Full name of the user
        email: Email address of the user
        phone: Phone number of the user
        is_admin: Boolean indicating if the user is an admin
        truck_count: Number of trucks associated with the user
        load_count: Number of loads associated with the user
    """
    column_exclude_list = ('_password', "alternative_id")
    # column_editable_list = ('fullname', 'email', 'phone', 'is_admin')
    form_excluded_columns = ('alternative_id', 'creation_time', 'update_time')
    form_extra_fields = {
        'password': PasswordField('Password')
    }

    # column to show number of trucks and loads for each user
    column_list = ('id', 'fullname', 'email', 'phone', 'is_admin', 'truck_count', 'load_count')

    column_formatters = {
        'truck_count': lambda v, c, m, p: len(m.truck),
        'load_count': lambda v, c, m, p: len(m.load),
    }
    
    # truck_count = Truck.query.filter_by(user_id=User.id).count()
    # load_count = Load.query.filter_by(user_id=User.id).count()
class LoadAdminView(ModelView):
    form_overrides = {
        'user_id': SelectField,
        'truck_id': SelectField,
    }

    # Force Flask-Admin to include these columns in the form
    form_columns = (
        'user_id',
        'truck_id',
        'pickup_location',
        'pickup_datetime',
        'pickup_contact_name',
        'pickup_contact_phone',
        'drop_location',
        'drop_datetime',
        'drop_contact_name',
        'drop_contact_phone',
        'load_type',
        'load_weight',
        'load_details',
        'load_current_location',
        'cost',
        'is_active',
        'in_progress'
    )

    def _user_choices(self):
        return [(u.id, u.fullname) for u in User.query.all()]

    def _truck_choices(self):
        return [(t.truck_id, t.vehicle_registration_number) for t in Truck.query.all()]

    def create_form(self, obj=None):
        form = super().create_form(obj)
        form.user_id.choices = self._user_choices()
        form.truck_id.choices = self._truck_choices()
        return form

    def edit_form(self, obj=None):
        form = super().edit_form(obj)
        form.user_id.choices = self._user_choices()
        form.truck_id.choices = self._truck_choices()
        return form

class TruckAdminView(ModelView):
    """Admin view for managing Truck records with restricted and editable fields."""

    # ---- Columns to show in list view ----
    column_list = (
        'truck_id',
        'user_id',
        'vehicle_registration_number',
        'vehicle_model_name',
        'vehicle_type',
        'vehicle_capacity',
        'current_location',
        'is_verified',
        'is_available'
    )

    # ---- Columns hidden from list or forms ----
    column_exclude_list = ('tds',)
    form_excluded_columns = ('truck_id', 'load', 'owner_pan', 'driver_license')

    # ---- Inline editable columns ----
    column_editable_list = ('is_verified', 'is_available', 'current_location')

    # ---- Dropdown for user selection ----
    form_overrides = {
        'user_id': SelectField,
        'vehicle_type': SelectField
    }

    # ---- Specify exactly which fields appear in Create/Edit forms ----
    form_columns = (
        'user_id',
        'vehicle_registration_number',
        'vehicle_model_name',
        'vehicle_type',
        'vehicle_capacity',
        'current_location',
        'vehicle_insurance',
        'owner_name',
        'owner_phone',
        'owner_aadhaar',
        'owner_pan',
        'driver_name',
        'driver_phone',
        'driver_aadhaar',
        'driver_license',
        'is_verified',
        'is_available'
    )

    # ---- Dropdown choice sources ----
    def _user_choices(self):
        return [(u.id, u.fullname) for u in User.query.all()]

    def _vehicle_type_choices(self):
        from app.constants.variable_constants import Truck_conts
        return Truck_conts.VEHICLE_TYPE_CHOICES

    # ---- Pre-fill dropdowns dynamically ----
    def create_form(self, obj=None):
        form = super().create_form(obj)
        form.user_id.choices = self._user_choices()
        form.vehicle_type.choices = self._vehicle_type_choices()
        return form

    def edit_form(self, obj=None):
        form = super().edit_form(obj)
        form.user_id.choices = self._user_choices()
        form.vehicle_type.choices = self._vehicle_type_choices()
        return form

    # ---- Business logic validations ----
    def on_model_change(self, form, model, is_created):
        """Ensure trucks always belong to a user and have valid registration."""
        if not model.user_id:
            raise ValueError("Each truck must be assigned to a user.")
        if not model.vehicle_registration_number:
            raise ValueError("Vehicle registration number is required.")
        if not model.vehicle_type:
            raise ValueError("Vehicle type is required.")
