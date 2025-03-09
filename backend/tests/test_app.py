import pytest, os, sys
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash
from datetime import date

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../flaskr')))
from flaskr import app, get_user_by_name, User, create_user, db

def test_client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SECRET_KEY'] = 'test_secret_key'
    
    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.drop_all()

@pytest.fixture(scope='module')
def init_database():
    with app.app_context():
        hashed_password = generate_password_hash("testpassword")
        user = User(username="testuser", password=hashed_password, email="testuser@example.com", birthdate=date(2000, 1, 1))
        db.session.add(user)
        db.session.commit()
        yield db
        db.session.remove()

def test_get_user_by_name(test_client, init_database):
    user = get_user_by_name("testuser")
    assert user is not None
    assert user['username'] == "testuser"
    assert user['email'] == "testuser@example.com"
    assert user['birthdate'] == "2000-01-01"

def test_get_user_by_name_not_found(test_client, init_database):
    user = get_user_by_name("nonexistentuser")
    assert user is None