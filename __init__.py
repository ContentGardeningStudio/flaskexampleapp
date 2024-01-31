from flask import Flask
from flask_sqlalchemy import SQLAlchemy
# from flask_login import LoginManager

from flask.cli import with_appcontext

# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()


def create_app():
    app = Flask(__name__)

    app.config["SECRET_KEY"] = "Jsucdupejmoaedpoqmvnlepas"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"

    db.init_app(app)

    # login_manager = LoginManager()
    # login_manager.login_view = "auth.login"
    # login_manager.init_app(app)

    # # blueprint for auth routes in our app
    # from .auth import auth as auth_blueprint
    #
    # app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    from .main import main as main_blueprint

    app.register_blueprint(main_blueprint)

    @app.cli.command("init-db")
    @with_appcontext
    def init_db_command():
        """Clear existing data and create new tables."""
        db.drop_all()
        db.create_all()
        print("Initialized the database.")

    return app
