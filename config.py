import os


class Config:
    """Base configuration."""

    SECRET_KEY = os.getenv("SECRET_KEY", "your_secret_key")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///app.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = False
    TESTING = False


class DevelopmentConfig(Config):
    """Development configuration."""

    SECRET_KEY = "Jsucdupejmoaedpoqmvnlepas"
    SQLALCHEMY_DATABASE_URI = "sqlite:///app.db"
    DEBUG = True
    SQLALCHEMY_ECHO = True  # Log SQL queries to stdout for debugging

    SECURITY_PASSWORD_SALT = os.getenv(
        "SECURITY_PASSWORD_SALT",
        "ab3d3a0f6984c4f5hkao41509b097a7bd498e903f3c9b2eea667h16",
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECURITY_REGISTERABLE = True
    SECURITY_CONFIRMABLE = True

    # mailtrap
    MAIL_SERVER = "sandbox.smtp.mailtrap.io"
    MAIL_PORT = 2525
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False


class TestingConfig(Config):
    """Testing configuration."""

    TESTING = True
    SQLALCHEMY_DATABASE_URI = (
        "sqlite:///:memory:"  # Use in-memory SQLite database for tests
    )
    WTF_CSRF_ENABLED = False  # Disable CSRF tokens in the Forms for testing


class ProductionConfig(Config):
    """Production configuration."""

    SECRET_KEY = os.getenv(
        "SECRET_KEY"
    )  # Expecting secret key to be set in environment variable
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL"
    )  # Expecting database URL to be set in environment variable
