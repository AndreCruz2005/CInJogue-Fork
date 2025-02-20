from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

from database.models import User, Game, UserLibary

def create_user(username, password, email, birthdate):
    try:
        hashed_password = generate_password_hash(password) 
        new_user = User(username=username, password=hashed_password, email=email, birthdate=birthdate)
        db.session.add(new_user)
        db.session.commit()
        return new_user
        
    except Exception as e:
        db.session.rollback() 
        print(f"Error creating user: {e}")
        return None

def login(username, password, session):
    user = get_user_by_name(username)
    if user and check_password_hash(user['password'], password):
        for k, v in user.items():
            session[k] = v
        return True
    return False

def get_user_by_name(username):
    user = db.session.query(User).filter_by(username=username).first()

    if user:
        return {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "birthdate": user.birthdate.strftime("%Y-%m-%d"),
            "password":user.password
        }
    return None

def remove_user(username):
    try:
        user = db.session.query(User).filter_by(username=username).first()

        if user:
            db.session.delete(user)
            db.session.commit()
            return True  
        return False

    except Exception as e:
        db.session.rollback() 
        print(f"Error removing user: {e}")
        return False
    
def create_game(title, data):
    try:
        new_game = Game(title=title, rating='UNPLAYED', state='UNPLAYED', data=data)
        db.session.add(new_game)
        db.session.commit()
        return new_game
        
    except Exception as e:
        db.session.rollback() 
        print(f"Error creating game: {e}")
        return None

def add_game_to_library(user_id, game_id):
    try:
        # Create the association in the user_library table
        new_entry = UserLibary.insert().values(user_id=user_id, game_id=game_id)
        
        # Execute the insertion
        db.session.execute(new_entry)
        
        # Commit the transaction
        db.session.commit()
        print(f"Game {game_id} added to user {user_id}'s library.")
        
    except Exception as e:
        db.session.rollback()
        print("Failed to add game: " + str(e))

