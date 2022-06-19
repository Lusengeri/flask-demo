import pytest
from main import create_app, clear_app_db
from api.config.config import TestingConfig
from api.utils.database import db

@pytest.fixture(scope='function')
def app():
    app = create_app(TestingConfig)
    app.app_context().push()
    yield app
    clear_app_db(app)

@pytest.fixture(scope='function', autouse=True)
def client(app):
    return app.test_client()
