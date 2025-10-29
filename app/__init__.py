from flask import Flask 
from sqlalchemy import MetaData
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from config import DevelopmentConfig, TestingConfig, ProductionConfig

from dotenv import load_dotenv
load_dotenv()

convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention= convention)
db = SQLAlchemy(metadata = metadata)
bcrypt = Bcrypt()
migrate = Migrate()
csrf = CSRFProtect()
login_manager = LoginManager() 
admin = Admin(template_mode='bootstrap4')

def create_app(
    config_class = TestingConfig
):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_class)

    @app.context_processor
    def inject_globals():
            return dict(
                GOOGLE_KEY = app.config['GOOGLE_KEY']
            )

    from .routes.admin import UserAdminView, AdminView, LoadAdminView, TruckAdminView

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db, render_as_batch= True)
    csrf.init_app(app)
    admin.init_app(app, index_view= AdminView())

    from .models import User, Truck, Load
    admin.add_view(UserAdminView(User, db.session))
    admin.add_view(TruckAdminView(Truck, db.session))
    admin.add_view(LoadAdminView(Load, db.session))

    with app.app_context():
        if app.config.get('TESTING_DATA'):
            db.create_all()
            make_admin_user(
                app.config.get('ADMIN_EMAIL'), 
                app.config.get('ADMIN_PASSWORD'), 
                User
            )
            make_testing_data(db)

    from .routes import landing, auth, booking, register, dashboard
    app.register_blueprint(landing.bp)
    app.register_blueprint(auth.bp)
    app.register_blueprint(booking.bp)
    app.register_blueprint(register.bp)
    app.register_blueprint(dashboard.bp)

    return app

# function to make a Admin user if not exists
def make_admin_user(admin_email, admin_password, User):
    """Create an admin user if not exists."""
    if admin_email and admin_password:
        admin_user = User.query.filter_by(email=admin_email).first()
        if not admin_user:
            admin_user = User(
                fullname= "Admin",
                email= admin_email,
                password= admin_password,
                is_admin=True
            )
            db.session.add(admin_user)
            db.session.commit()
            print(f"Admin user created with email: {admin_email}")
        else:
            print(f"Admin user already exists with email: {admin_email}")
    else:
        print("ADMIN_EMAIL environment variable not set. Cannot create admin user.")

# function to populate testing data
def make_testing_data(db):
    print("Populating testing data...")
    import json
    from .models import Truck, Load, User

    with open("./testing_data.json", 'r') as file:
        testing_data = json.load(file)

    truck_testing_data = testing_data["trucks"]
    load_testing_data = testing_data["loads"]

    def make_get_user(user_id: int):
        email = f"test_user{user_id}@example.com"
        user = User.query.filter_by(id=user_id, email=email).first()
        if user:
            print(f"user:{user_id} with email: {email} already exists.")
            return user
        else:
            user = User(
                id= user_id,
                fullname= f"Test User {user_id}",
                email= email,
                password= "password",
                is_admin=False
            )
            db.session.add(user)
            print(f"user created{user_id} and email: {email}")
            return user

    for truck_data in truck_testing_data:
        user = make_get_user(truck_data['user_id'])

        existing_truck = Truck.query.filter_by(
            user_id = user.id,
            vehicle_registration_number=truck_data['vehicle_registration_number']).first()
        if existing_truck:
            print(f"Truck with registration number {truck_data['vehicle_registration_number']} for user_id {user.id} already exists. Skipping.")
            continue
        else:
            print(f"Truck created with registration number {truck_data['vehicle_registration_number']} for user_id {user.id}.")
            truck = Truck(**truck_data)
            db.session.add(truck)

    for load_data in load_testing_data:
        user = make_get_user(load_data['user_id'])

        from datetime import datetime
        if 'pickup_datetime' in load_data and 'drop_datetime' in load_data:
            load_data['pickup_datetime'] = datetime.fromisoformat(load_data['pickup_datetime'])
            load_data['drop_datetime'] = datetime.fromisoformat(load_data['drop_datetime'])

        existing_load = Load.query.filter_by(
            user_id= user.id,
            pickup_contact_name=load_data['pickup_contact_name']).first()
        if existing_load:
            print(f"Load with pickup contact name {load_data['pickup_contact_name']} for user_id {load_data['user_id']} already exists. Skipping.")
            continue
        else:
            print(f"Load created with pickup contact name {load_data['pickup_contact_name']} for user_id {load_data['user_id']}.")
            load = Load(**load_data)
            db.session.add(load)

    db.session.commit()
    print("Finished populating testing data.")