from flask import (
    Blueprint,
    render_template, request,
    flash,
    redirect,
    url_for,
    session
)
from flask_login import login_required, current_user, logout_user, login_user

from app import login_manager, bcrypt, db
from app.form import SignupForm, LoginForm
from app.models import User
from app.constants.session_keys import SessionKeys
from app.constants.variable_constants import User_conts
from app.utils import _autofill_db_dict
from sqlalchemy import or_, and_


bp = Blueprint(
    "auth", 
    __name__, 
    url_prefix='/auth',
    template_folder='templates'
)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@bp.route('/signup', methods=['POST', 'GET'])
def signup():
    signup_form = SignupForm(request.form)

    if signup_form.validate_on_submit():
        # Clean up the phone before saving
        phone_raw = getattr(signup_form, User_conts.PHONE).data
        clean_phone = ''.join([c for c in str(phone_raw) if c.isdigit()])
        setattr(signup_form, User_conts.PHONE, clean_phone)

        user = _autofill_db_dict(input_data=signup_form.data, database_class=User)
        db.session.add(user)
        db.session.commit()

        login_user(user)
        flash(f'Account successfully created under {getattr(signup_form, User_conts.FULLNAME).data}', 'success')
        return redirect(url_for('landing.index'))

    return render_template(
        'signup.html',
        signup_form = signup_form
    )

# @bp.route('/login', methods=["POST", "GET"])
# def login():
#     login_form = LoginForm(request.form)
#     if login_form.validate_on_submit():
#         user: User = User.query.filter(
#             (User.email == getattr(login_form, User_conts.EMAIL).data) |
#             (User.phone == getattr(login_form, User_conts.PHONE).data)
#         ).first()
#         print(user)
#         if user:
#             if user.check_password(getattr(login_form, User_conts.PASSWORD).data):
#                 flash(f"Welcome back, {user.fullname}", "success")
#                 login_user(user)
#             else:
#                 flash("Invalid password", "danger")
#                 return redirect(url_for("auth.login")) 
#             if session.get(SessionKeys.PENDING_FORM_DATA):
#                 return redirect(f'/booking/{session[SessionKeys.BOOKING_TYPE]}')
#             return redirect(url_for('landing.index'))

#         else:
#             flash(f"No user with Email:{getattr(login_form, User_conts.EMAIL).data} and Phone:{getattr(login_form, User_conts.PHONE).data}", 'danger')
#             return redirect(url_for('auth.signup'))

#     if request.method == 'POST':
#         print(login_form.errors)

#     return render_template(
#         'login.html',
#         login_form = login_form
#     )
@bp.route('/login', methods=["POST", "GET"])
def login():
    login_form = LoginForm(request.form)

    if login_form.validate_on_submit():
        email_input = getattr(login_form, User_conts.EMAIL).data.strip().lower()
        phone_input = getattr(login_form, User_conts.PHONE).data.strip()
        password_input = getattr(login_form, User_conts.PASSWORD).data

        # Normalize phone: remove +, spaces, etc.
        clean_phone = ''.join([c for c in phone_input if c.isdigit()])

        # Try to find a user with both matching email and phone
        user = User.query.filter(
            and_(
        User.email == email_input,
        or_(User.phone == clean_phone, User.phone == '+' + clean_phone)
    )
).first()

        # Case 1️⃣: No user found → check what was wrong
        if not user:
            # Check separately to give clear error messages
            user_email_exists = User.query.filter_by(email=email_input).first()
            user_phone_exists = User.query.filter_by(phone=clean_phone).first()

            if not user_email_exists and not user_phone_exists:
                flash(f"No account found with Email '{email_input}' and Phone '{clean_phone}'.", "danger")
            elif not user_email_exists:
                flash(f"Incorrect email '{email_input}' for this phone number.", "danger")
            elif not user_phone_exists:
                flash(f"Incorrect phone number '{clean_phone}' for this email.", "danger")

            return redirect(url_for("auth.login"))

        # Case 2️⃣: User exists but password wrong
        if not user.check_password(password_input):
            flash("Incorrect password. Please try again.", "danger")
            return redirect(url_for("auth.login"))

        # Case 3️⃣: All correct → login success
        login_user(user)
        flash(f"Welcome back, {user.fullname}!", "success")

        # Redirect logic
        if session.get(SessionKeys.PENDING_FORM_DATA):
            return redirect(f"/booking/{session[SessionKeys.BOOKING_TYPE]}")
        return redirect(url_for("landing.index"))

    # If form didn't validate (e.g., phone format)
    if request.method == "POST":
        print(login_form.errors)

    return render_template("login.html", login_form=login_form)

@bp.route('/logout')
@login_required
def logout():
    flash(f'Logged out successfully from {current_user.fullname}', 'info')
    logout_user()
    session.clear()
    return redirect(url_for('landing.index'))