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
    SECRET_KEY = os.environ.get('SECRET_KEY')
    if not SECRET_KEY:
        raise ValueError("SECRET_KEY environment variable is not set. App cannot start.")
    SESSION_COOKIE_NAME = 'your_session'
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)

    # Database
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Security
    WTF_CSRF_ENABLED = True

    GOOGLE_KEY = os.getenv('GOOGLE_KEY')
    ADMIN_EMAIL = os.getenv('ADMIN_EMAIL')
    ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD')
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-5.4")

    # Email — uses Gmail SMTP to send emails
    MAIL_SERVER = 'smtp.gmail.com'   # Gmail's post office address
    MAIL_PORT = 587                  # Port 587 = secure TLS connection
    MAIL_USE_TLS = True              # Encrypt the connection
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_USERNAME')

class DevelopmentConfig(Config):
    DEBUG = True
    FLASK_ADMIN_SWATCH = "litera"
    SQLALCHEMY_DATABASE_URI = (
        os.environ.get("DEV_DATABASE_URL")
        or f"sqlite:///{os.path.join(basedir, 'instance/dev.db')}"
    )

class TestingConfig(Config):
    TESTING = True
    RESET = False
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(basedir, 'instance/test.db')}"
    TESTING_DATA = True
    WTF_CSRF_ENABLED = False  # Disable CSRF for testing


class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = (
        os.environ.get("DATABASE_URL")
        or f"sqlite:///{os.path.join(basedir, 'instance/prod.db')}"
    )

