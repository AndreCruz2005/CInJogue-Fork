import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../backend/flaskr')))
from app import create_app

@pytest.fixture
def app():
    app = create_app("sqlite://")
    app.config['TESTING'] = True
    
    yield app

@pytest.fixture
def client(app):
    return app.test_client()