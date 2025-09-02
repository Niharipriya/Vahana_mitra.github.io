from flask import (
    Blueprint,
    session, 
    render_template,
    flash,
    redirect,
    url_for
)
from flask_login import current_user, login_required

from app.constants.session_keys import SessionKeys
from app.form import LoadRegistrationForm, TruckRegistrationForm
from app.utils import autofill_fields

bp = Blueprint(
    'register',
    __name__,
    url_prefix='/register',
    template_folder='templates'
)

@bp.route('/truck/<int:id>', methods=['POST', 'GET'])
@login_required
def truck(id: int):
    # Prefill form from session if available
    form = TruckRegistrationForm(
        data=autofill_fields(
            'truck-',
            session.get(SessionKeys.PENDING_FORM_DATA, {}),
            TruckRegistrationForm()
        )
    )

    if form.validate_on_submit():
        print("Adding truck…")
        truck = autofill_db_dict(form.data, Truck)

        # ✅ assign foreign key to current user
        truck.user_id = current_user.user_id

        db.session.add(truck)
        db.session.commit()
        flash("Truck registered successfully!", "success")

        return redirect(url_for("landing.index"))

    return render_template("truck_registration_form.html", form=form)


@bp.route('/load/<int:id>', methods=['POST', 'GET'])
@login_required
def load(id: int):
    # Prefill form from session if available
    form = LoadRegistrationForm(
        data=autofill_fields(
            'load-',
            session.get(SessionKeys.PENDING_FORM_DATA, {}),
            LoadRegistrationForm()
        )
    )

    if form.validate_on_submit():
        print("Adding load…")
        load = autofill_db_dict(form.data, Load)

        # ✅ assign foreign key to current user
        load.user_id = current_user.user_id

        db.session.add(load)
        db.session.commit()
        flash("Load registered successfully!", "success")

        return redirect(url_for("landing.index"))

    return render_template("load_registration_form.html", form=form)
