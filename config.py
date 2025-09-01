import os
import json
from datetime import timedelta
from dotenv import load_dotenv

# Load .env file if present
load_dotenv()

# Base Directory
basedir = os.path.abspath(os.path.dirname(__file__))

# Load testing data (if needed by seeds)
with open(os.path.join(basedir, "testing_data.json"), "r") as file:
    testing_data = json.load(file)

truck_testing_data = testing_data.get("trucks", [])
load_testing_data = testing_data.get("loads", [])


class Config:
    """Base configuration (shared across environments)."""

    # General
    SECRET_KEY = os.getenv("SECRET_KEY", "your-default-secret-key")
    SESSION_COOKIE_NAME = "your_session"
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)

    # Database
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Security
    WTF_CSRF_ENABLED = True

    # Google Maps API Key
    GOOGLE_KEY = os.getenv("GOOGLE_MAPS_API_KEY")

    # Admin credentials
    ADMIN_EMAIL = os.getenv("ADMIN_EMAIL")


class DevelopmentConfig(Config):
    DEBUG = True
    FLASK_ADMIN_SWATCH = "litera"
    SQLALCHEMY_DATABASE_URI = (
        os.getenv("DEV_DATABASE_URL")
        or f"sqlite:///{os.path.join(basedir, 'instance', 'dev.db')}"
    )


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = (
        os.getenv("TEST_DATABASE_URL") or "sqlite:///:memory:"
    )
    WTF_CSRF_ENABLED = False  # Disable CSRF for testing


class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = (
        os.getenv("DATABASE_URL")
        or f"sqlite:///{os.path.join(basedir, 'instance', 'prod.db')}"
    )
