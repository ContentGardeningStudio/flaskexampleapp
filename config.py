import os

class Config:
    """Base configuration."""
    SECRET_KEY = os.getenv('SECRET_KEY', 'your_secret_key')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = False
    TESTING = False

class DevelopmentConfig(Config):
    """Development configuration."""
    SECRET_KEY = "Jsucdupejmoaedpoqmvnlepas"
    SQLALCHEMY_DATABASE_URI = "sqlite:///app.db"
    DEBUG = True
    SQLALCHEMY_ECHO = True  # Log SQL queries to stdout for debugging

class TestingConfig(Config):
    """Testing configuration."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'  # Use in-memory SQLite database for tests
    WTF_CSRF_ENABLED = False  # Disable CSRF tokens in the Forms for testing

class ProductionConfig(Config):
    """Production configuration."""
    SECRET_KEY = os.getenv('SECRET_KEY')  # Expecting secret key to be set in environment variable
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')  # Expecting database URL to be set in environment variable
