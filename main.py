from models import *
from form import SignupForm, LoginForm, TruckRegistrationForm, MaterialRegistrationForm, TruckRequestForm, MaterialRequestForm
from config import DevelopmentConfig

import json
from flask import Flask, render_template, url_for, request, flash, redirect, session
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_user, logout_user, current_user, login_required

with open("./testing_data.json", 'r') as file:
    testing_data = json.load(file)

truck_testing_data = testing_data["trucks"]
load_testing_data = testing_data["loads"]

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
ADMIN = 'admin@gmail.com'

db.init_app(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'profile'

# region BOOT ROUTINE

@app.before_request
def create_table():
    """Generates database, adds testing data to the database, and admin as a user"""
    db.create_all()

    [Truck.from_json(data= x) for x in truck_testing_data] 
    [Load.from_json(data= y) for y in load_testing_data]

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

@app.route("/", methods=['POST', 'GET'])
def _():
    """Redirect to landing"""
    return redirect(url_for('landing'))

#endregion

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route("/landing", methods=['POST', 'GET'])
def landing():
    """Landing page has about form to request truck and material"""
    truck_request_form = TruckRequestForm()
    material_request_form = MaterialRequestForm()

    def not_profile_redirect(form_type, form):
        """redirect to profile if not logged in else redirect to booking

        Args:
            form_type (str): name of the form requested
            form (WTForm): the form object
        """
        if not current_user.is_authenticated:
            session['pending_form_data'] = {
                'form_type': form_type,
                'data': form.data,
                'timestamp': datetime.now().isoformat()
            }
            flash("Please Login or SignUp to continue your booking process", "danger")
            return redirect(url_for('profile'))
        print("redirected to booking")
        return redirect(url_for('booking'))

    if material_request_form.validate_on_submit():
        list_compatible_loads = Load.find_available_materials(
            capacity= material_request_form.capacity.data,
            current_location= material_request_form.current_location.data
        )

        load_ids = [load.load_id for load in list_compatible_loads]
        session['compatible_load_ids'] = load_ids
        return not_profile_redirect('material_request_form', material_request_form)

    elif truck_request_form.validate_on_submit():
        list_compatible_truck = Truck.find_available_truck(
            location= truck_request_form.pickup_location.data,
            min_capacity= truck_request_form.estimated_weight.data,
            # truck_type= truck_request_form.truck_type.data,
        )

        truck_ids = [truck.truck_id for truck in list_compatible_truck]
        session['compatible_truck_ids'] = truck_ids
        return not_profile_redirect('truck_request_form', truck_request_form)

    if request.method == 'POST':
        print(truck_request_form.errors)

    return render_template("landing.html", material_request_form = material_request_form, truck_request_form=truck_request_form)

@app.route("/admin", methods=['POST', 'GET'])
@login_required
def admin():
    truck_registration_form = TruckRegistrationForm()
    material_registration_form = MaterialRegistrationForm()
    if current_user.email != ADMIN:
        flash('Access denied please login as admin', 'danger')
        return redirect(url_for('profile'), form= 'login')

    users = User.query.all()
    return render_template(
        'admin.html',
        users = users,
        truck_registration_form = truck_registration_form,
        material_registration_form = material_registration_form
    )

@app.route("/admin/<int:user_id>/materials", methods=['GET'])
def show_materials(user_id):
    material_list = Load.get_by_user(user_id)
    return render_template(
        "tabs.html",
        list_type = "material",
        loads = material_list
    )
@app.route("/admin/<int:user_id>/trucks", methods=['GET'])
def show_trucks(user_id):
    truck_list = Truck.get_by_user(user_id)
    return render_template(
        "tabs.html",
        list_type = "truck",
        trucks = truck_list
    )

@app.route("/booking", methods=['POST', 'GET'])
def booking():
    list_compatible = []
    booking_type = ""

    if session.get('compatible_truck_ids'):
        truck_ids = session.pop('compatible_truck_ids', [])
        list_compatible = Truck.query.filter(Truck.truck_id.in_(truck_ids)).all()
        booking_type = "truck"
    elif session.get('compatible_load_ids'):
        load_ids = session.pop('compatible_load_ids', [])
        list_compatible = Load.query.filter(Load.load_id.in_(load_ids)).all()
        booking_type = "load"

    return render_template("booking.html", list_compatible=list_compatible, booking_type=booking_type)

@app.route("/signup_login", methods=['POST', 'GET'])
def profile():
    """
    <input type="tel" id="phone" name="phone" class="form-control" placeholder="Phone Number">
    <input type="hidden" name="full_phone" id="full_phone">
    <input type="hidden" name="country_code" id="country_code">
    """
    form_type = request.args.get('form_type', 'signup')
    signup_form = SignupForm()
    login_form = LoginForm()

    # print("Form submitted:", request.method == 'POST')
    # print("Form validation status:", signup_form.validate_on_submit())
    # print("Form errors:", signup_form.errors)

    if signup_form.validate_on_submit():
        # Set phone data from hidden field
        signup_form.phone.data = request.form.get('full_phone')
        hashed_password = bcrypt.generate_password_hash(signup_form.password.data).decode('utf-8')
        user = User(
            fullname = signup_form.fullname.data,
            password_hash = hashed_password,
            email = signup_form.email.data,
            phone = request.form.get('full_phone'),
        )
        db.session.add(user)
        db.session.commit()
        flash('Account created successfully. You can login now', 'success')
        return redirect(url_for('profile', form_type='login'))

    elif login_form.validate_on_submit():
        _user: User = User.query.filter_by(email = login_form.email.data).first()
        if _user and _user.check_password(login_form.password.data, bcrypt):
            login_user(_user)
            flash('Login Successfully', 'success')
            if _user.email == ADMIN:
                return redirect(url_for('admin'))
            elif session.get('compatible_truck_ids') or session.get('compatible_load_ids'):
                return redirect(url_for('booking'))
            else:
                return redirect(url_for('dashboard'))
        else:
            flash('Login failed. Check your email or password.', 'danger')

    if request.method == 'POST':
        print(signup_form.errors)

    return render_template("signup_login.html", form_type=form_type, signup_form=signup_form, login_form=login_form)

@app.route("/register/<string:booking_type>/<int:id>", methods=['POST', 'GET'])
def register(booking_type, id):
    form = MaterialRegistrationForm() if booking_type == 'truck' else TruckRegistrationForm()
    return render_template("register.html", form=form )

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
    flash(f'Logged out successfully from {current_user.fullname}', 'info')
    logout_user()
    return redirect(url_for('profile'))

@app.route("/tabs")
def view_tabs():
    trucks = Truck.query.all()
    loads = Load.query.all()
    return render_template("tabs.html", trucks=trucks, loads=loads)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)

