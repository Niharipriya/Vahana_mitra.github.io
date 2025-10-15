from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app.models import Load  # Make sure this path is correct for your project

bp = Blueprint("dashboard", __name__, url_prefix="/dashboard")

@bp.route("/")
@login_required
def index():
    # Fetch loads that belong to the logged-in user
    user_loads = Load.query.filter_by(user_id=current_user.id).all()

    return render_template(
        "dashboard.html",
        current_user=current_user,
        loads=user_loads,
        adding_type=None,
        truck_form=None,
        material_form=None
    )
