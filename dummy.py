import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from tabledef import *

engine = create_engine('sqlite:///student.db', echo=True)

# create a Session
Session = sessionmaker(bind=engine)
session = Session()

# Create objects
user = Student("james","James","Boogie","MIT")
session.add(user)

user = Student("lara","Lara","Miami","UU")
session.add(user)

user = Student("eric","Eric","York","Stanford")
session.add(user)

# commit the record the database
session.commit()


# fermer la session avec close
# with car cst un contxt manager
# with Session() as session:
#   mettre tt jusqu'a la ligne commit
# ainsi python va faire close pour nous