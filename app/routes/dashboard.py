from flask import (
    Blueprint,
    render_template
)

from flask_login import login_required

bp = Blueprint(
    "dashboard",
    __name__,
    url_prefix="/dashboard"
)

@bp.route("/")
@login_required
def index():
    
    return render_template(
        "dashboard.html"
    )