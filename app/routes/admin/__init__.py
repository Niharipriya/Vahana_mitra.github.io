from flask_login import current_user
from flask import flash, redirect, url_for
from flask_admin import AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView
from wtforms import PasswordField

from app import admin
from app.models import User, Truck, Load

class AdminView(AdminIndexView):

    @expose('/')
    def index(self):
        return redirect(url_for('landing.index'))

    def is_accessible(self):
        """Check if the current user is an admin."""
        return current_user.is_authenticated and current_user.is_admin

    def inaccessible_callback(self, name, **kwargs):
        """Redirect to login page if the user doesn't have access."""
        flash("You do not have permission to access the admin panel.", "danger")
        return redirect(url_for('auth.login'))

class UserAdminView(ModelView):
    """Admin view for the User model."""
    column_exclude_list = ('_password', "alternative_id")
    column_editable_list = ('fullname', 'email', 'phone', 'is_admin')
    form_excluded_columns = ('alternative_id', 'creation_time', 'update_time')
    form_extra_fields = {
        'password': PasswordField('Password')
    }
