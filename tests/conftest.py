import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../backend/flaskr')))
from app import create_app
from app import *


@pytest.fixture
def app():
    app = create_app("sqlite://")
    app.config['TESTING'] = True    
    
    with app.app_context():
        new_game = Game(title="game1", data="{mock: data}")
        db.session.add(new_game)
        db.session.commit()
    
    return app.test_client()

@pytest.fixture
def client(app):
    # Criar usuários de teste
    app.post('/signup', json={"username": "John Doe", "password": "JohnDoePass", "email":"e@gmail.com", "birthdate":"2000-01-01"})
    app.post('/signup', json={"username": "Zezinho", "password": "ZezinhoPass", "email":"ze@gmail.com", "birthdate":"1950-11-10"})
    
    
    return app
    