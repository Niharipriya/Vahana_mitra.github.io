from flask import (
      Blueprint,
      render_template,
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
from app.utils import autofill_db_dict

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
      signup_form = SignupForm()
      if signup_form.validate_on_submit():
            hashed_password = bcrypt.generate_password_hash(
                getattr(signup_form, User_conts.PASSWORD).data).decode('utf-8')
            # user = User(
            #       fullname = signup_form.fullname.data,
            #       password_hash = hashed_password,
            #       email = signup_form.email.data,
            #       phone = signup_form.phone.data
            # )
            signup_form_data = signup_form.data
            signup_form_data[User_conts.PASSWORD] = hashed_password
            user = autofill_db_dict(
                  signup_form_data,
                  User
            )
            db.session.add(user)
            db.session.commit()
            flash(f'Account successfully under {getattr(signup_form, User_conts.FULLNAME).data}', 'success')
            return redirect(url_for('auth.login'))

      return render_template(
            'signup.html',
            signup_form = signup_form
      )

@bp.route('/login', methods=["POST", "GET"])
def login():
      login_form = LoginForm()
      if login_form.validate_on_submit():
            user: User = User.query.filter_by(
                  email = getattr(login_form, User_conts.EMAIL).data,
                  phone = getattr(login_form, User_conts.PHONE).data
            ).first()
            if bcrypt.check_password_hash(
                        getattr(user, user.attribute_map()[User_conts.PASSWORD]),
                        getattr(login_form, User_conts.PASSWORD).data
                  ):
                  login_user(user)
            if session.get(SessionKeys.PENDING_FORM_DATA):
                  return redirect(f'/booking/{session[SessionKeys.BOOKING_TYPE]}')
            return redirect(url_for('landing.index'))

      return render_template(
            'login.html',
            login_form = login_form
      )

@bp.route('/logout')
@login_required
def logout():
    flash(f'Logged out successfully from {getattr(current_user, User.attribute_map(current_user)[User_conts.FULLNAME])}', 'info')
    logout_user()
    return redirect(url_for('landing.index'))