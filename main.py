from models import *
from form import SignupForm, LoginForm, TruckRegistrationForm, MaterialRegistrationForm, TruckRequestForm, MaterialRequestForm
from config import DevelopmentConfig
import random, string, os
from dotenv import load_dotenv
load_dotenv()

import enum
from flask import Flask, render_template, url_for, request, flash, redirect, session, jsonify
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_user, logout_user, current_user, login_required

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)

db.init_app(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'profile'

def generate_random_pass():
    length = 13
    chars = string.ascii_letters + '!@#$%^&*()' + string.digits
    random.seed = (os.urandom(1024))

    return ''.join(random.choice(chars) for i in range(length))

class User_Auth(enum.Enum):
    ANONYMOUS = enum.auto()
    AUNTHETICATED = enum.auto()
    UNAUNTHETICATED = enum.auto()
    ADMIN = enum.auto()
class Booking_Type(enum.Enum):
    TRUCK = 'truck'
    MATERIAL = 'material'
class Booking_State(enum.Enum):
    IN_PROGRESS = enum.auto()
    COMPLETE = enum.auto()
# region BOOT ROUTINE

@app.before_request
def create_table():
    """Generates database, adds testing data to the database, and admin as a user"""
    db.create_all()

    email_check = User.query.filter_by(email=os.environ.get('ADMIN_EMAIL')).first()
    if not email_check:
        ADMIN = User(
            fullname = os.environ.get('ADMIN_USERNAME'),
            password_hash = bcrypt.generate_password_hash(os.environ.get('ADMIN_PASSWORD')).decode('utf-8'),
            email = os.environ.get('ADMIN_EMAIL'),
            phone = os.environ.get('ADMIN_PHONE'),
        )
        db.session.add(ADMIN)
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

    def not_profile_redirect(form):
        """redirect to profile if not logged in else redirect to booking"""
        if not current_user.is_authenticated:
            session['pending_form_data'] = form.data
            flash("Please Login or SignUp to continue your booking process", "danger")
            return redirect(url_for('profile'))
        print("redirected to booking")
        return redirect(url_for('booking', booking_type = session['BOOKING_TYPE']))

    if material_request_form.validate_on_submit():
        session['BOOKING_TYPE'] = Booking_Type.MATERIAL
        list_compatible_loads = Load.find_available_materials(
            capacity= material_request_form.capacity.data,
            current_location= material_request_form.current_location.data
        )

        load_ids = [load.load_id for load in list_compatible_loads]
        session['compatible_load_ids'] = load_ids
        return not_profile_redirect(material_request_form)

    elif truck_request_form.validate_on_submit():
        session['BOOKING_TYPE'] = Booking_Type.TRUCK
        list_compatible_truck = Truck.find_available_truck(
            location= truck_request_form.pickup_location.data,
            min_capacity= truck_request_form.estimated_weight.data,
            # truck_type= truck_request_form.truck_type.data,
        )

        truck_ids = [truck.truck_id for truck in list_compatible_truck]
        session['compatible_truck_ids'] = truck_ids
        return not_profile_redirect(truck_request_form)

    if request.method == 'POST':
        print(truck_request_form.errors)
    
    return render_template(
        "landing.html", 
        material_request_form = material_request_form, 
        truck_request_form=truck_request_form, 
        GOOGLE_KEY = app.config.get('GOOGLE_KEY')
    )

@app.route("/testing", methods=['POST', 'GET'])
def testing_stuff():
    
    return render_template('testing.html', GOOGLE_KEY = os.environ.get('GOOGLE_KEY'))

@app.route("/admin", methods=['POST', 'GET'])
@login_required
def admin():
    truck_registration_form = TruckRegistrationForm()
    material_registration_form = MaterialRegistrationForm()
    if current_user.email != app.config.get('ADMIN_EMAIL'):
        flash('Access denied please login as admin', 'danger')
        return redirect(url_for('profile'), form= 'login')

    if truck_registration_form.validate_on_submit():
        user = User.query.filter_by(email=truck_registration_form.user_email.data).first()
        if user:
            user_id = user.user_id
        else:
            hashed_password = bcrypt.generate_password_hash(generate_random_pass()).decode('utf-8')
            new_user = User(
                fullname = truck_registration_form.user_fullname.data,
                password_hash = hashed_password,
                email = truck_registration_form.user_email.data,
                phone = truck_registration_form.user_phone.data,
            )
            db.session.add(new_user)
            db.session.commit()
            user_id = new_user.user_id
        truck = Truck(
            user_id = user_id,
            registration_number = truck_registration_form.registration_number.data,
            model_name = truck_registration_form.model.data,
            type = truck_registration_form.type.data,
            capacity = truck_registration_form.capacity.data,
            current_location = truck_registration_form.current_location.data,
            owner_name = truck_registration_form.owner_name.data, 
            owner_mobile = truck_registration_form.owner_name.data, 
            owner_aadhaar = truck_registration_form.owner_aadhaar.data,
            owner_pan = truck_registration_form.owner_pan.data,
            owner_tos = truck_registration_form.owner_tos.data,
        )
        db.session.add(truck)
        db.session.commit()
        print("Added trucks to db")
        print(truck_registration_form.data)

        flash(f"Successfully Created a material request for the user {material_registration_form.user_fullname.data}", "success")
        return redirect(url_for('admin'))

    elif material_registration_form.validate_on_submit():
        user = User.query.filter_by(email=material_registration_form.user_email.data).first()
        if user:
            user_id = user.user_id
        else:
            hashed_password = bcrypt.generate_password_hash(generate_random_pass()).decode('utf-8')
            new_user = User(
                fullname = material_registration_form.user_fullname.data,
                password_hash = hashed_password,
                email = material_registration_form.user_email.data,
                phone = material_registration_form.user_phone.data,
            )
            db.session.add(new_user)
            db.session.commit()
            user_id = new_user.user_id

        load = Load(
            user_id = user_id,
            type = material_registration_form.material_type.data,
            weight = material_registration_form.estimated_weight.data,
            details = material_registration_form.material_details.data,

            pickup_address = material_registration_form.pickup_location.data,
            pickup_date = material_registration_form.pickup_date.data,
            pickup_contact_name = material_registration_form.pickup_contact_name.data,
            pickup_contact_phone = material_registration_form.pickup_contact_phone.data,

            drop_address = material_registration_form.drop_location.data,
            drop_date = material_registration_form.drop_date.data,
            drop_contact_name = material_registration_form.drop_contact_name.data,
            drop_contact_phone = material_registration_form.drop_contact_phone.data,
        )
        db.session.add(load)
        db.session.commit()
        print("Added materials to db")
        print(material_registration_form.data)

        flash(f"Successfully Created a material request for the user {material_registration_form.user_fullname.data}", "success")
        return redirect(url_for('admin'))
    if request.method == 'POST':
        print("ERROR")
        print(material_registration_form.data)
        print(material_registration_form.errors)

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

@app.route("/booking/<string:booking_type>", methods=['POST', 'GET'])
def booking(booking_type):
    list_compatible = []

    if session.get('compatible_truck_ids') and booking_type == 'material':
        truck_ids = session.pop('compatible_truck_ids', [])
        list_compatible = Truck.query.filter(Truck.truck_id.in_(truck_ids)).all()
    elif session.get('compatible_load_ids') and booking_type == 'truck':
        load_ids = session.pop('compatible_load_ids', [])
        list_compatible = Load.query.filter(Load.load_id.in_(load_ids)).all()

    print(booking_type)

    return render_template(
        "booking.html", 
        booking_type=booking_type,
        list_compatible=list_compatible, 
    )

@app.route("/register/<string:booking_type>/<int:id>", methods=['POST', 'GET'])
def register(booking_type, id):
    form = None
    pending_data = session['pending_form_data']['data']
    print(pending_data)
    if booking_type == 'material':
        form = MaterialRegistrationForm()
        form.pickup_location.data = pending_data['pickup_location']
        form.drop_location.data = pending_data['drop_location']
        form.estimated_weight.data = pending_data['estimated_weight']
        form.truck_type.data = pending_data['truck_type']

    elif booking_type == 'truck':
        form = TruckRegistrationForm()

    if form.validate_on_submit():
        redirect(url_for('dashboard'))

    return render_template('user_register.html', booking_type=booking_type, form=form)

@app.route('/dashboard', methods=['POST', 'GET'])
@login_required
def dashboard():
    if current_user.email == app.config.get('ADMIN_EMAIL'):
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

@app.route("/tabs")
def view_tabs():
    trucks = Truck.query.all()
    loads = Load.query.all()
    return render_template("tabs.html", trucks=trucks, loads=loads)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)

