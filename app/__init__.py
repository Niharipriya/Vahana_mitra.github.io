from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from config import DevelopmentConfig

from dotenv import load_dotenv
load_dotenv()

db = SQLAlchemy()
bcrypt = Bcrypt()
migrate = Migrate()
csrf = CSRFProtect()
login_manager = LoginManager() 
admin = Admin(template_mode='bootstrap4')

def create_app(
      config_class = DevelopmentConfig
):
      app = Flask(__name__, instance_relative_config=True)
      app.config.from_object(config_class)

      db.init_app(app)
      bcrypt.init_app(app)
      login_manager.init_app(app)
      migrate.init_app(app, db)
      csrf.init_app(app)
      admin.init_app(app)

      from .models import User, Truck, Load
      admin.add_view(ModelView(User, db.session))
      admin.add_view(ModelView(Truck, db.session))
      admin.add_view(ModelView(Load, db.session))

      from .routes import landing, auth, booking, register
      app.register_blueprint(landing.bp)
      app.register_blueprint(auth.bp)
      app.register_blueprint(booking.bp)
      app.register_blueprint(register.bp)

      return app