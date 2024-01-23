from flask import Flask, render_template, request, redirect, flash, jsonify
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

app = Flask(__name__)
engine = create_engine('sqlite:///url.db', echo=False)
# create a Session
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()

class Url(Base):
    """"""
    __tablename__ = "url"

    id = Column(Integer, primary_key=True)
    url = Column(String)
    description = Column(String)
    category = Column(String)

    def __init__(self, url, description, category):
        self.url = url
        self.description = description
        self.category = category


# create tables
Base.metadata.create_all(engine)


@app.route("/")
def index():
    urls = session.query(Url).all()
    return render_template("index.html", urls=urls)


@app.route('/new', methods=['GET', 'POST'])
def create():
    if request.method == 'GET':
        return render_template('create.html')
    if request.method == 'POST':
        url = request.form["url"]
        description = request.form["description"]
        category = request.form["category"]
        url = Url(url=url, description=description, category=category)
        session.add(url)
        session.commit()
        return redirect('/')


@app.route("/<int:id>")
def show(id):
    url = session.get(Url, id)
    return render_template("show.html", url=url)

@app.route("/update/<int:id>", methods = ['GET','POST'])
def update(id):
    url = session.get(Url, id)
    if request.method == 'POST':
        if url:
            session.delete(url)
            session.commit()

            url = request.form["url"]
            description = request.form["description"]
            category = request.form["category"]
            url = Url(url=url, description=description, category=category)
            session.add(url)
            session.commit()
            return redirect('/')
        else:
            return f"Url with id = {id} Does not exist"
 
    return render_template('update.html', url=url)


@app.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete(id):
    url = session.get(Url, id)
    if request.method == 'POST':
        if url:
            session.delete(url)
            session.commit()
            return redirect('/')

    return render_template('delete.html', url=url)


if __name__ == '__main__':
    app.run(debug=True)