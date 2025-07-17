from models import *
from form import SignupForm, LoginForm, TruckRegistrationForm, MaterialRegistrationForm

from flask import Flask, render_template, url_for, request, flash, redirect
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_user, logout_user, current_user, login_required

app = Flask(__name__)
app.config['SECRET_KEY'] = 'TempSecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
ADMIN = 'admin@gmail.com'

db.init_app(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'profile'

@app.before_request
def create_table():
    db.create_all()
    email_check = User.query.filter_by(email=ADMIN).first()
    if not email_check:
        hashed_password = bcrypt.generate_password_hash("admin1234").decode('utf-8')
        user = User(
            fullname = "Admin",
            password_hash = hashed_password,
            email = ADMIN
        )
        db.session.add(user)
        db.session.commit()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route("/")
@app.route("/landing", methods=['POST', 'GET'])
def landing():
    material_request_form = MaterialRegistrationForm()
    truck_request_form = TruckRegistrationForm()

    if material_request_form.validate_on_submit():
        flash("Request successfully accepted", 'success')
        redirect(url_for('landing'))
    elif truck_request_form.validate_on_submit():
        flash("Request successfully accepted", 'success')
        redirect(url_for('landing'))
    return render_template("landing.html", material_request_form = material_request_form, truck_request_form=truck_request_form)

@app.route("/signup_login", methods=['POST', 'GET'])
def profile():
    form_type = request.args.get('form', 'signup')
    signup_form = SignupForm()
    login_form = LoginForm()

    if form_type == 'signup':
        if signup_form.validate_on_submit():
            hashed_password = bcrypt.generate_password_hash(signup_form.password.data).decode('utf-8')
            user = User(
                fullname = signup_form.fullname.data,
                password_hash = hashed_password,
                email = signup_form.email.data,
                phone = request.form.get('full_phone')
,
            )
            db.session.add(user)
            db.session.commit()
            flash('Account created successfully. You can login now', 'success')
            redirect(url_for('profile', form='login'))

    elif form_type == 'login':
        if login_form.validate_on_submit():
            _user: User = User.query.filter_by(email = login_form.email.data).first()
            if _user and _user.check_password(login_form.password.data, bcrypt):
                login_user(_user)
                flash('Login Successfully', 'success')
                return redirect(url_for('admin')) if _user.email == ADMIN else redirect(url_for('dashboard'))
            else:
                flash('Login failed. Check your email or password.', 'danger')

    return render_template("signup_login.html", form_type=form_type, signup_form=signup_form, login_form=login_form)

@app.route('/dashboard', methods=['POST', 'GET'])
@login_required
def dashboard():
    if current_user.email == ADMIN:
        return redirect(url_for('admin'))

    adding_type = request.args.get('adding', 'truck')
    truck_form = TruckRegistrationForm()
    material_form = MaterialRegistrationForm()
    trucks = Truck.query.filter_by(user_id=current_user.user_id).all()
    materials = Load.query.filter_by(user_id=current_user.user_id).all()

    if adding_type == 'truck':
        if truck_form.validate_on_submit():
            truck = Truck(
                user_id = current_user.user_id,
                truck_name = truck_form.truck_name.data,
                truck_details = truck_form.truck_registration_number.data,
                availability = truck_form.availability.data,
            )
            db.session.add(truck)
            db.session.commit()
            flash(f"{truck_form.truck_name.data} added successfully to your {current_user.fullname}", 'success')
            return redirect(url_for('dashboard', adding='truck'))
        if request.method == 'POST':
            print(truck_form.errors)
    elif adding_type == 'material':
        if material_form.validate_on_submit():
            material = Load(
                user_id = current_user.user_id,
                load_details = material_form.load_name.data,
                pickup_address = material_form.pickup_address.data,
                drop_address = material_form.drop_address.data
            )
            db.session.add(material)
            db.session.commit()
            flash(f"{material_form.load_name.data} added successfully to your {current_user.fullname}", 'success')
            return redirect(url_for('dashboard', adding='material'))
        if request.method == 'POST':
            print(material_form.errors)
    return render_template('dashboard.html', current_user=current_user, adding_type=adding_type, truck_form=truck_form, material_form=material_form, trucks=trucks)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully.', 'info')
    return redirect(url_for('profile'))

@app.route("/tabs")
def view_tabs():
    trucks = Truck.query.all()
    loads = Load.query.all()
    return render_template("tabs.html", trucks=trucks, loads=loads)


@app.route("/admin")
@login_required
def admin():
    if current_user.email != ADMIN:
        flash('Access denied please login as admin', 'danger')
        return redirect(url_for('profile'), form= 'login')

    user = User.query.all()
    return render_template('admin.html', users=user)
 
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)

