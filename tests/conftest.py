import pytest
from flaskexampleapp import create_app
from flaskexampleapp import db as _db

@pytest.fixture(scope='module')
def app():
    """
    Create and configure a new app instance for each test.
    """
    # Note: Adjust create_app to load your test config
    app = create_app('testing')
    return app

@pytest.fixture(scope='module')
def client(app):
    """
    A test client for the app.
    """
    return app.test_client()

@pytest.fixture(scope='module')
def db(app):
    """
    A database for the tests.
    """
    _db.app = app
    _db.create_all()

    yield _db

    _db.drop_all()
