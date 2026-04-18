from flask import (
    Blueprint,
    render_template, request,
    flash,
    redirect,
    url_for,
    session
)
from flask_login import login_required, current_user, logout_user, login_user

import logging
from app import login_manager, db
from app.email_utils import send_verification_email, verify_token

logger = logging.getLogger(__name__)
from app.form import SignupForm, LoginForm
from app.models import User
from app.constants.session_keys import SessionKeys
from app.constants.variable_constants import User_conts
from app.utils import _autofill_db_dict


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
        getattr(signup_form, User_conts.PHONE).data = ''.join([c for c in str(phone_raw) if c.isdigit()])

        user = _autofill_db_dict(input_data=signup_form.data, database_class=User)
        db.session.add(user)
        db.session.commit()

        # Send verification email — user must click link before logging in
        try:
            send_verification_email(user.email)
            flash('Account created! Please check your email to verify your account.', 'info')
        except Exception as e:
            logger.error("Failed to send verification email to %s: %s", user.email, e)
            flash('Account created but we could not send a verification email. Contact support.', 'warning')

        return redirect(url_for('auth.login'))

    return render_template(
        'signup.html',
        signup_form = signup_form
    )

@bp.route('/login', methods=["POST", "GET"])
def login():
    login_form = LoginForm(request.form)
    if login_form.validate_on_submit():
        email = login_form.user_email.data
        phone = login_form.user_phone.data
        user: User = (
            User.query.filter_by(email=email).first() if email
            else User.query.filter_by(phone=phone).first()
        )
        logger.debug("Login attempt for user: %s", user)
        if user:
            if not user.check_password(getattr(login_form, User_conts.PASSWORD).data):
                flash("Invalid password", "danger")
                return redirect(url_for("auth.login"))

            # Block login if email not verified yet
            if not user.is_email_verified:
                flash("Please verify your email before logging in. Check your inbox.", "warning")
                return redirect(url_for("auth.login"))

            login_user(user)
            flash(f"Welcome back, {user.fullname}", "success")
            if session.get(SessionKeys.PENDING_FORM_DATA):
                return redirect(url_for('booking.booking', booking_type=session.get(SessionKeys.BOOKING_TYPE, 'Load')))
            return redirect(url_for('landing.index'))

        else:
            flash(f"No user with Email:{getattr(login_form, User_conts.EMAIL).data} and Phone:{getattr(login_form, User_conts.PHONE).data}", 'danger')
            return redirect(url_for('auth.signup'))

    if request.method == 'POST':
        logger.warning("Login form errors: %s", login_form.errors)

    return render_template(
        'login.html',
        login_form = login_form
    )
# @bp.route('/login', methods=["POST", "GET"])
# def login():
#     login_form = LoginForm(request.form)

#     if login_form.validate_on_submit():
#         email_input = getattr(login_form, User_conts.EMAIL).data.strip().lower()
#         phone_input = getattr(login_form, User_conts.PHONE).data.strip()
#         password_input = getattr(login_form, User_conts.PASSWORD).data

#         # Normalize phone: remove +, spaces, etc.
#         clean_phone = ''.join([c for c in phone_input if c.isdigit()])

#         # Try to find a user with both matching email and phone
#         user = User.query.filter(
#             and_(
#         User.email == email_input,
#         or_(User.phone == clean_phone, User.phone == '+' + clean_phone)
#     )
# ).first()

#         # Case 1️⃣: No user found → check what was wrong
#         if not user:
#             # Check separately to give clear error messages
#             user_email_exists = User.query.filter_by(email=email_input).first()
#             user_phone_exists = User.query.filter_by(phone=clean_phone).first()

#             if not user_email_exists and not user_phone_exists:
#                 flash(f"No account found with Email '{email_input}' and Phone '{clean_phone}'.", "danger")
#             elif not user_email_exists:
#                 flash(f"Incorrect email '{email_input}' for this phone number.", "danger")
#             elif not user_phone_exists:
#                 flash(f"Incorrect phone number '{clean_phone}' for this email.", "danger")

#             return redirect(url_for("auth.login"))

#         # Case 2️⃣: User exists but password wrong
#         if not user.check_password(password_input):
#             flash("Incorrect password. Please try again.", "danger")
#             return redirect(url_for("auth.login"))

#         # Case 3️⃣: All correct → login success
#         login_user(user)
#         flash(f"Welcome back, {user.fullname}!", "success")

#         # Redirect logic
#         if session.get(SessionKeys.PENDING_FORM_DATA):
#             return redirect(f"/booking/{session[SessionKeys.BOOKING_TYPE]}")
#         return redirect(url_for("landing.index"))

#     # If form didn't validate (e.g., phone format)
#     if request.method == "POST":
#         logger.warning("Login form errors: %s", login_form.errors)

#     return render_template("login.html", login_form=login_form)

@bp.route('/verify/<token>')
def verify_email(token):
    """
    User clicks the link in their email → lands here.
    We decode the token to get their email, find them in DB,
    mark is_email_verified = True, then let them log in.
    """
    email = verify_token(token)

    if email is None:
        flash("This verification link has expired or is invalid. Please sign up again.", "danger")
        return redirect(url_for("auth.signup"))

    user = User.query.filter_by(email=email).first()
    if not user:
        flash("No account found for this link.", "danger")
        return redirect(url_for("auth.signup"))

    if user.is_email_verified:
        flash("Your email is already verified. Please log in.", "info")
        return redirect(url_for("auth.login"))

    user.is_email_verified = True
    db.session.commit()
    flash("Email verified successfully! You can now log in.", "success")
    return redirect(url_for("auth.login"))


@bp.route('/resend-verification')
def resend_verification():
    """
    If user didn't get the email, they can request a new one.
    """
    email = request.args.get('email')
    if not email:
        flash("No email provided.", "danger")
        return redirect(url_for("auth.login"))

    user = User.query.filter_by(email=email).first()
    if not user:
        flash("No account found with that email.", "danger")
        return redirect(url_for("auth.signup"))

    if user.is_email_verified:
        flash("Your email is already verified.", "info")
        return redirect(url_for("auth.login"))

    try:
        send_verification_email(user.email)
        flash("Verification email resent! Please check your inbox.", "success")
    except Exception as e:
        logger.error("Failed to resend verification email to %s: %s", user.email, e)
        flash("Could not send email. Please try again later.", "danger")

    return redirect(url_for("auth.login"))


@bp.route('/logout')
@login_required
def logout():
    flash(f'Logged out successfully from {current_user.fullname}', 'info')
    logout_user()
    session.clear()
    return redirect(url_for('landing.index'))