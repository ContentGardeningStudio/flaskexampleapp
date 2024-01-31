from flask_login import UserMixin

from . import db


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password_hash = db.Column(db.String, nullable=False)
    # authenticated = db.Column(db.Boolean, default=False)

    def __init__(self, username, password, email):
        self.username = username
        self.email = email
        self.password_hash = password

    def is_active(self):
        """True, as all users are active."""
        return True

    def get_id(self):
        """Return the email address to satisfy Flask-Login's requirements."""
        return self.email

    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return self.authenticated

    def is_anonymous(self):
        """False, as anonymous users aren't supported."""
        return False


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    urls = db.relationship(
        "Url", backref=db.backref("category", lazy=True)
    )

    def __init__(self, name):
        self.name = name


class Url(db.Model):
    """Url model"""

    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String)
    description = db.Column(db.String)
    # category = db.Column(db.String(80))
    category_id = db.Column(
        db.Integer, db.ForeignKey("category.id"), nullable=False
    )

    def __init__(self, url, description, category):
        self.url = url
        self.description = description
        self.category = category
