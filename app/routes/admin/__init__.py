from flask_login import current_user
from flask import flash, redirect, url_for
from flask_admin import AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView
from wtforms import PasswordField

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
        """Redirect to login page if the user doesn't have access."""
        flash("You do not have permission to access the admin panel.", "danger")
        return redirect(url_for('auth.login'))

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
    column_editable_list = ('fullname', 'email', 'phone', 'is_admin')
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
