from flask import Blueprint, redirect, render_template, request
from . import db
from .models import Category, Url

# @app.teardown_appcontext
# def shutdown_session(exception=None):
#     db.session.remove()



main = Blueprint("main", __name__)


@main.route("/url")
def show_all_url():
    urls = db.session.query(Url).all()
    return render_template("index.html", urls=urls)


# @main.route("/users")
# def show_all_users():
#     users = db.session.query(User).all()
#     return render_template("users.html", users=users)


@main.route("/category")
def show_all_categories():
    categories = db.session.query(Category).all()
    return render_template("categories.html", categories=categories)


@main.route("/new_category", methods=["GET", "POST"])
def add_category():
    if request.method == "GET":
        return render_template("create_cat.html")
    if request.method == "POST":
        name = request.form["name"]
        category = Category(name=name)
        db.session.add(category)
        db.session.commit()
        return redirect("/category")


# @main.route("/new_user", methods=["GET", "POST"])
# def add_user():
#     if request.method == "GET":
#         return render_template("create_user.html")
#     if request.method == "POST":
#         username = request.form["username"]
#         email = request.form["email"]
#         password = request.form["password"]
#         user = User(username=username, password=password, email=email)
#         db.session.add(user)
#         db.session.commit()
#         return redirect("/users")


@main.route("/new_url", methods=["GET", "POST"])
def create():
    categories = db.session.query(Category).all()
    if request.method == "GET":
        return render_template("create_url.html", categories=categories)
    if request.method == "POST":
        url = request.form["url"]
        description = request.form["description"]
        # category = request.form["category"]
        category_id = request.form.get("category_id")
        category = Category.query.get(category_id)
        url = Url(url=url, description=description, category=category)
        db.session.add(url)
        db.session.commit()
        return redirect("/")


@main.route("/category/<int:id>")
def show_one_category(id):
    category = db.session.get(Category, id)
    return render_template("show_cat.html", category=category)


@main.route("/url/<int:id>")
def show(id):
    url = db.session.get(Url, id)
    return render_template("show_url.html", url=url)


@main.route("/url/update/<int:id>", methods=["GET", "POST"])
def update(id):
    url = db.session.get(Url, id)
    if request.method == "POST":
        if url:
            db.session.delete(url)
            db.session.commit()

            url = request.form["url"]
            description = request.form["description"]
            category = request.form["category"]
            url = Url(url=url, description=description, category=category)
            db.session.add(url)
            db.session.commit()
            return redirect("/")
        else:
            return f"Url with id = {id} Does not exist"

    return render_template("update_url.html", url=url)


@main.route("/url/delete/<int:id>", methods=["GET", "POST"])
def delete(id):
    url = db.session.get(Url, id)
    if request.method == "POST":
        if url:
            db.session.delete(url)
            db.session.commit()
            return redirect("/")

    return render_template("delete_url.html", url=url)
