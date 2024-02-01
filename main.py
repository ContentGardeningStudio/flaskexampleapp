from flask import Blueprint, redirect, render_template, request, url_for
from . import db
from .models import Category, Url

# @app.teardown_appcontext
# def shutdown_session(exception=None):
#     db.session.remove()


main = Blueprint("main", __name__)

@main.route('/')
def index():
    return render_template('index.html')


@main.route('/profile')
def profile():
    return render_template('auth/profile.html')


@main.route("/url")
def show_all_url():
    urls = db.session.query(Url).all()
    return render_template("url/index.html", urls=urls)


# @main.route("/users")
# def show_all_users():
#     users = db.session.query(User).all()
#     return render_template("users.html", users=users)


@main.route("/category")
def show_all_categories():
    categories = db.session.query(Category).all()
    return render_template("category/categories.html", categories=categories)


@main.route("/new_category", methods=["GET", "POST"])
def add_category():
    if request.method == "GET":
        return render_template("category/create_cat.html")
    if request.method == "POST":
        name = request.form.get("name")
        category = Category(name=name)
        db.session.add(category)
        db.session.commit()
        return redirect(url_for('main.show_all_categories'))


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
        return render_template("url/create.html", categories=categories)
    if request.method == "POST":
        url = request.form.get("url")
        description = request.form.get("description")
        category_id = request.form.get("category_id")
        category = Category.query.get(category_id)
        url = Url(url=url, description=description, category=category)
        db.session.add(url)
        db.session.commit()
        return redirect(url_for('main.show_all_url'))


@main.route("/category/<int:id>")
def show_one_category(id):
    category = db.session.get(Category, id)
    if category:
        return render_template("category/show_cat.html", category=category)
    else:
        return f"Category with id {id} does not exist"


@main.route("/url/<int:id>")
def show(id):
    url = db.session.get(Url, id)
    if url:
        return render_template("url/show.html", url=url)
    else:
        return f"Url with id {id} does not exist"


@main.route("/url/update/<int:id>", methods=["GET", "POST"])
def update(id):
    url = db.session.get(Url, id)
    categories = Category.query.all()
    if request.method == "POST":
        if url:
            db.session.delete(url)
            db.session.commit()

            url = request.form.get("url")
            description = request.form.get("description")
            category_id = request.form.get("category_id")
            category = Category.query.get(category_id)
            url = Url(url=url, description=description, category=category)
            db.session.add(url)
            db.session.commit()
            return redirect(url_for('main.show_all_url'))
        else:
            return f"Url with id = {id} Does not exist"

    return render_template("url/update.html", url=url, categories=categories)


@main.route("/category/update/<int:id>", methods=["GET", "POST"])
def update_category(id):
    category = db.session.get(Category, id)
    if request.method == "POST":
        if category:
            db.session.delete(category)
            db.session.commit()

            name = request.form.get("name")
            category = Category(name=name)
            db.session.add(category)
            db.session.commit()
            return redirect(url_for('main.show_all_categories'))
        else:
            return f"Url with id = {id} Does not exist"

    return render_template("category/update_cat.html", category=category)


@main.route("/url/delete/<int:id>", methods=["GET", "POST"])
def delete(id):
    url = db.session.get(Url, id)
    if request.method == "POST":
        if url:
            db.session.delete(url)
            db.session.commit()
            return redirect(url_for('main.show_all_url'))

    return render_template("url/delete.html", url=url)


@main.route("/category/delete/<int:id>", methods=["GET", "POST"])
def delete_category(id):
    category = db.session.get(Category, id)
    if request.method == "POST":
        if category:
            db.session.delete(category)
            db.session.commit()
            return redirect(url_for('main.show_all_categories'))

    return render_template("category/delete_cat.html", category=category)