from flask import Flask, redirect, render_template, request, url_for, flash, Blueprint
import sqlalchemy
from flask.cli import with_appcontext
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, current_user, login_user, logout_user, login_required
from urllib.parse import urlsplit
import sqlalchemy.orm as so

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SECRET_KEY"] = "Jsucdupejmoaedpoqmvnlepas"
db = SQLAlchemy(app)
login = LoginManager()
login.login_view = "login"
login.init_app(app)


@app.teardown_appcontext
def shutdown_session(exception=None):
    db.session.remove()


@login.user_loader
def load_user(id):
    return db.session.get(User, id)


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


##############################################
class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    urls = db.relationship('Url', backref=db.backref('category', lazy=True))

    def __init__(self, name):
        self.name = name

##############################################
class Url(db.Model):
    """Url model"""

    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String)
    description = db.Column(db.String)
    # category = db.Column(db.String(80))
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    # category = db.relationship('Category', backref=db.backref('posts', lazy=True))

    def __init__(self, url, description, category):
        self.url = url
        self.description = description
        self.category = category



with app.app_context():
    # Create tables within an application context
    db.create_all()


@app.cli.command("init-db")
@with_appcontext
def init_db_command():
    """Clear existing data and create new tables."""
    db.drop_all()
    db.create_all()
    print("Initialized the database.")


auth = Blueprint('auth', __name__)
@auth.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")

    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')

        # if this returns a user, then the email already exists in database
        user = User.query.filter_by(email=email, username=username).first()

        # if a user is found, we want to redirect back to signup page so user can try again
        if user:
            flash("Please choose another email or username")
            return redirect(url_for('register'))

        # create a new user with the form data. Hash the password so the plaintext version isn't saved.
        new_user = User(username=username, email=email, password=generate_password_hash(password))

        # add the new user to the database
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('login'))


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "GET":
        return render_template("login.html")

    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False

        user = User.query.filter_by(username=username).first()

        # check if the user actually exists
        # take the user-supplied password, hash it, and compare it to the hashed password in the database
        if not user or not check_password_hash(user.password_hash, password):
            flash('Please check your login details and try again.')
            # if the user doesn't exist or password is wrong, reload the page
            return redirect(url_for('login'))

        # if the above check passes, then we know the user has the right credentials
        login_user(user, remember=remember)
        return redirect(url_for('home'))


@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@auth.route('/')
@login_required
def home():
    return render_template("profile.html", current_user=current_user)

main = Blueprint('main', __name__)
@main.route("/url")
def show_all_url():
    urls = db.session.query(Url).all()
    return render_template("url.html", urls=urls)


@main.route("/users")
def show_all_users():
    users = db.session.query(User).all()
    return render_template("users.html", users=users)

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


@main.route("/new_user", methods=["GET", "POST"])
def add_user():
    if request.method == "GET":
        return render_template("create_user.html")
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        user = User(username=username, password=password, email=email)
        db.session.add(user)
        db.session.commit()
        return redirect("/users")


@main.route("/new_url", methods=["GET", "POST"])
def create():
    categories = db.session.query(Category).all()
    if request.method == "GET":
        return render_template("create_url.html", categories=categories)
    if request.method == "POST":
        url = request.form["url"]
        description = request.form["description"]
        # category = request.form["category"]
        category_id = request.form.get('category_id')
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


if __name__ == "__main__":
    app.run(debug=True)
