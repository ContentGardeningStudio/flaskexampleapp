from urllib.parse import urlsplit

import sqlalchemy
import sqlalchemy.orm as so
from flask import (Blueprint, Flask, flash, redirect, render_template, request,
                   url_for)
from flask.cli import with_appcontext
from flask_login import (LoginManager, UserMixin, current_user, login_required,
                         login_user, logout_user)
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash

from . import db
from .models import User


@login.user_loader
def load_user(id):
    return db.session.get(User, id)


auth = Blueprint("auth", __name__)


@auth.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        email = request.form.get("email")

        # if this returns a user, then the email already exists in database
        user = User.query.filter_by(email=email, username=username).first()

        # if a user is found, we want to redirect back to signup page so user can try again
        if user:
            flash("Please choose another email or username")
            return redirect(url_for("register"))

        # create a new user with the form data. Hash the password so the plaintext version isn't saved.
        new_user = User(
            username=username, email=email, password=generate_password_hash(password)
        )

        # add the new user to the database
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for("login"))


@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        remember = True if request.form.get("remember") else False

        user = User.query.filter_by(username=username).first()

        # check if the user actually exists
        # take the user-supplied password, hash it, and compare it to the hashed password in the database
        if not user or not check_password_hash(user.password_hash, password):
            flash("Please check your login details and try again.")
            # if the user doesn't exist or password is wrong, reload the page
            return redirect(url_for("login"))

        # if the above check passes, then we know the user has the right credentials
        login_user(user, remember=remember)
        return redirect(url_for("home"))


@auth.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("login"))


# @auth.route('/')
# @login_required
# def home():
#     return render_template("profile.html", current_user=current_user)
