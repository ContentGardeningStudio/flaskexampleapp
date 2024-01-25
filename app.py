from flask import Flask, redirect, render_template, request

from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
db = SQLAlchemy(app)

@app.teardown_appcontext
def shutdown_session(exception=None):
    db.session.remove()


class Url(db.Model):
    """Url model"""

    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String)
    description = db.Column(db.String)
    category = db.Column(db.String(80))

    def __init__(self, url, description, category):
        self.url = url
        self.description = description
        self.category = category


with app.app_context():
    # Create tables within an application context
    db.create_all()


@app.route("/")
def index():
    urls = db.session.query(Url).all()
    return render_template("index.html", urls=urls)


@app.route("/new", methods=["GET", "POST"])
def create():
    if request.method == "GET":
        return render_template("create.html")
    if request.method == "POST":
        url = request.form["url"]
        description = request.form["description"]
        category = request.form["category"]
        url = Url(url=url, description=description, category=category)
        db.session.add(url)
        db.session.commit()
        return redirect("/")


@app.route("/<int:id>")
def show(id):
    url = db.session.get(Url, id)
    return render_template("show.html", url=url)


@app.route("/update/<int:id>", methods=["GET", "POST"])
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

    return render_template("update.html", url=url)


@app.route("/delete/<int:id>", methods=["GET", "POST"])
def delete(id):
    url = db.session.get(Url, id)
    if request.method == "POST":
        if url:
            db.session.delete(url)
            db.session.commit()
            return redirect("/")

    return render_template("delete.html", url=url)


if __name__ == "__main__":
    app.run(debug=True)
