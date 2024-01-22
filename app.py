from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request, redirect, flash
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from tabledef import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///student.db'
db = SQLAlchemy(app)

engine = create_engine('sqlite:///student.db', echo=False)
# create a Session
Session = sessionmaker(bind=engine)
session = Session()

with app.app_context():
    db.create_all()

@app.route("/")
def index():
    students = session.query(Student).all()
    # students = Student.query.all()
    return render_template("index.html", students=students)


@app.route('/new', methods=['GET', 'POST'])
def create():
    if request.method == 'GET':
        return render_template('create.html')
    if request.method == 'POST':
        username = request.form["username"]
        firstname = request.form["firstname"]
        lastname = request.form["lastname"]
        university = request.form["university"]
        student = Student(username=username, firstname=firstname, lastname=lastname, university=university)
        session.add(student)
        session.commit()
        return redirect('/')


@app.route("/<int:id>")
def show(id):
    # student = Student.query.get(id)
    student = session.get(Student, id)
    return render_template("show.html", student=student)

@app.route("/update/<int:id>", methods = ['GET','POST'])
def update(id):
    student = session.get(Student, id)
    if request.method == 'POST':
        if student:
            session.delete(student)
            session.commit()
 
            username = request.form["username"]
            firstname = request.form["firstname"]
            lastname = request.form["lastname"]
            university = request.form["university"]
            student = Student(username=username, firstname=firstname, lastname=lastname, university=university)
 
            session.add(student)
            session.commit()
            return redirect('/')
        return f"Student with id = {id} Does not exist"
 
    return render_template('update.html', student = student)


@app.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete(id):
    student = session.get(Student, id)
    if request.method == 'POST':
        if student:
            session.delete(student)
            session.commit()
            return redirect('/')
        # abort(404)

    return render_template('delete.html', student=student)


if __name__ == '__main__':
    app.run(debug=True)