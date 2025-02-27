from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

from database.models import User, Game, UserLibrary, UserRecommendations

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

def log_user_in(username, password, session):
    user = get_user_by_name(username)
    if user and check_password_hash(user['password'], password):
        for k, v in user.items():
            session[k] = v
        return user
    return None

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
        new_game = Game(title=title, data=data)
        db.session.add(new_game)
        db.session.commit()
        return new_game
        
    except Exception as e:
        db.session.rollback() 
        print(f"Error creating game: {e}")
        return None

def add_game_to_library(user_id, game):
    try:
        new_entry = UserLibrary.insert().values(user_id=user_id, game_id=game.id, rating=0, state='UNPLAYED')
        db.session.execute(new_entry)
        db.session.commit()
        print(f"Game {game.title} added to user {user_id}'s library.")
        
    except Exception as e:
        db.session.rollback()
        print("Failed to add game: " + str(e))


def add_game_to_recommendations(user_id, game):
    try:
        new_entry = UserRecommendations.insert().values(user_id=user_id, game_id=game.id)
        db.session.execute(new_entry)
        db.session.commit()
        print(f"Game {game.title} added to user {user_id}'s recommendations.")
        
    except Exception as e:
        db.session.rollback()
        print("Failed to add game: " + str(e))
        

def remove_game_from_library(user_id, game_id):
    try:
        entry_to_delete = UserLibrary.delete().where(UserLibrary.c.user_id == user_id, UserLibrary.c.game_id == game_id)
        db.session.execute(entry_to_delete)
        db.session.commit()
        print(f"Game {game_id} removed from user {user_id}'s library.")
        
    except Exception as e:
        db.session.rollback()
        print("Failed to remove game: " + str(e))


def update_game_rating(user_id, game_id, new_rating):
    try:
        stmt = db.update(UserLibrary).where((UserLibrary.c.user_id == user_id) & (UserLibrary.c.game_id == game_id)
        ).values(rating=new_rating)

        db.session.execute(stmt)
        db.session.commit()
        print(f"Game {game_id}'s rating changed to {new_rating}")
        
    except Exception as e:
        db.session.rollback()
        print("Failed to update rating: " + str(e))

    
def update_game_state(user_id, game_id, new_state):
    try:
        stmt = db.update(UserLibrary).where((UserLibrary.c.user_id == user_id) & (UserLibrary.c.game_id == game_id)
        ).values(state=new_state)

        db.session.execute(stmt)
        db.session.commit()
        print(f"Game {game_id}'s state changed to {new_state}")
        
    except Exception as e:
        db.session.rollback()
        print("Failed to update state: " + str(e))
    
def get_libary(user_id):
    items = db.session.query(Game, UserLibrary.c.rating, UserLibrary.c.state)\
                                .join(UserLibrary)\
                                .filter(UserLibrary.c.user_id == user_id)\
                                .all()
    return items

def get_recommendations(user_id):
    games = db.session.query(Game).join(UserRecommendations).filter(UserLibrary.c.user_id == user_id).all()
    return games 