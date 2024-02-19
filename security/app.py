import os
from flask import Flask
from flask_security import SQLAlchemySessionUserDatastore, Security
from dotenv import load_dotenv
from database import db
from auth import User, Role
from flask_mailman import Mail
from flask_security import login_required

load_dotenv()

app = Flask(__name__)

app.config["SECRET_KEY"] = os.environ.get(
    "SECRET_KEY", "0aedgaii451cef0af8bd6432ec4b317c8999a9f8g77f5f3cb49fb9a8acds51d"
)
app.config["SECURITY_PASSWORD_SALT"] = os.environ.get(
    "SECURITY_PASSWORD_SALT",
    "ab3d3a0f6984c4f5hkao41509b097a7bd498e903f3c9b2eea667h16",
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECURITY_REGISTERABLE"] = True
app.config["SECURITY_CONFIRMABLE"] = True

# mailtrap
app.config['MAIL_SERVER'] = 'sandbox.smtp.mailtrap.io'
app.config['MAIL_PORT'] = 2525
app.config['MAIL_USERNAME'] = '22d11b67bc7943'
app.config['MAIL_PASSWORD'] = '07425b916f8383'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
mail = Mail(app)

uri = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_DATABASE_URI"] = uri
db.init_app(app)
user_datastore = SQLAlchemySessionUserDatastore(db.session, User, Role)
security = Security(app, user_datastore)


@app.route("/")
def home():
    return "Hello, world!"


@app.route("/protected")
@login_required
def protected():
    return "You're logged in!"
