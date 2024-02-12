from flask import (Blueprint, flash, redirect, render_template, request,
                   url_for)
from flask_login import (current_user, login_user, logout_user)
from werkzeug.security import check_password_hash, generate_password_hash

from . import db
from .models import User


auth = Blueprint("auth", __name__)


@auth.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "GET":
        return render_template("auth/signup.html")

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        email = request.form.get("email")
        age = request.form.get("age")

        # if this returns a user, then the email already exists in database
        user = User.query.filter_by(email=email, username=username).first()

        # if a user is found, we want to redirect back to signup page so user can try again
        if user:
            flash("Please choose another email or username")
            return redirect(url_for("auth.signup"))

        # create a new user with the form data. Hash the password so the plaintext version isn't saved.
        new_user = User(
            username=username, email=email, password=generate_password_hash(password), age=age
        )

        # add the new user to the database
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for("auth.login"))


@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("auth/login.html")

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
            return redirect(url_for("auth.login"))

        # if the above check passes, then we know the user has the right credentials
        login_user(user, remember=remember)
        return render_template("auth/profile.html", current_user=current_user)


@auth.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("auth.login"))