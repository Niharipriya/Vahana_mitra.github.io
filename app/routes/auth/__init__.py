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
            hashed_password = bcrypt.generate_password_hash(signup_form.password.data).decode('utf-8')
            user = User(
                  fullname = signup_form.fullname.data,
                  password = hashed_password,
                  email = signup_form.email.data,
                  phone = signup_form.phone.data
            )
            # signup_form_data = signup_form.data
            # signup_form_data['password'] = hashed_password
            # user = autofill_db_dict(
            #       signup_form_data,
            #       User
            # )
            db.session.add(user)
            db.session.commit()
            flash(f'Account successfully under {signup_form.fullname.data}', 'success')
            return redirect(url_for('auth.login'))

      return render_template(
            'signup.html',
            signup_form = signup_form
      )

@bp.route('/login', methods=["POST", "GET"])
def login():
      login_form = LoginForm()
      if login_form.validate_on_submit():
            user = User.query.filter_by(
                  email = login_form.email.data,
                  phone = login_form.phone.data
            ).first()
            if bcrypt.check_password_hash(user.password, login_form.password.data):
                  login_user(user)
                  
                  if session.get(SessionKeys.PENDING_FORM_DATA):
                        return redirect(f'/booking/{session.get(SessionKeys.BOOKING_TYPE)}')
                  return redirect(url_for('landing.index'))

      return render_template(
            'login.html',
            login_form = login_form
      )

@bp.route('/logout')
@login_required
def logout():
    flash(f'Logged out successfully from {current_user.fullname}', 'info')
    logout_user()
    return redirect(url_for('landing.index'))