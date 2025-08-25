import os, json
from datetime import timedelta

# Base Directory
basedir = os.path.abspath(os.path.dirname(__file__))
with open("./testing_data.json", 'r') as file:
    testing_data = json.load(file)

truck_testing_data = testing_data["trucks"]
load_testing_data = testing_data["loads"]

class Config:
    # General
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-default-secret-key'
    SESSION_COOKIE_NAME = 'your_session'
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)

    # Database
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Security
    WTF_CSRF_ENABLED = True

    # Email (for password reset etc.)
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER')
    GOOGLE_KEY = os.environ.get('GOOGLE_KEY')

    #Admin credentials
    ADMIN_EMAIL = os.environ.get('ADMIN_EMAIL')

class DevelopmentConfig(Config):
    DEBUG = True
    FLASK_ADMIN_SWATCH = "litera"
    SQLALCHEMY_DATABASE_URI = (
        os.environ.get("DEV_DATABASE_URL")
        or f"sqlite:///{os.path.join(basedir, 'instance/dev.db')}"
    )

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = (
        os.environ.get("TEST_DATABASE_URL") or "sqlite:///:memory:"
    )
    WTF_CSRF_ENABLED = False  # Disable CSRF for testing


class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = (
        os.environ.get("DATABASE_URL")
        or f"sqlite:///{os.path.join(basedir, 'instance/prod.db')}"
    )