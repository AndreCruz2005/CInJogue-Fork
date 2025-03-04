from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from database.game import *
from database.user import *

def add_game_to_library(user_id, game_id):
    try:
        new_entry = UserLibrary.insert().values(user_id=user_id, game_id=game_id, rating=0, state='UNPLAYED')
        db.session.execute(new_entry)
        db.session.commit()
        print(f"Game {game_id} added to user {user_id}'s library.")
        
    except Exception as e:
        db.session.rollback()
        print("Failed to add game to library: " + str(e))
        
def get_game_by_name(title):
    game = db.session.query(Game).filter_by(title=title).first()
    if game:
        return {
            "id": game.id,
            "title": game.title,
            "data": game.data
        }
    return None

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
        
def remove_game_from_recommendations(user_id, game_id):
    try:
        entry_to_delete = UserRecommendations.delete().where(UserRecommendations.c.user_id == user_id, UserRecommendations.c.game_id == game_id)
        db.session.execute(entry_to_delete)
        db.session.commit()
        print(f"Game {game_id} removed from user {user_id}'s recommendations.")
        
    except Exception as e:
        db.session.rollback()
        print("Failed to remove game: " + str(e))        

def clear_user_recommendations(user_id):
    db.session.query(UserRecommendations).filter_by(user_id=user_id).delete()
    db.session.commit()

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
    games = db.session.query(Game).join(UserRecommendations).filter(UserRecommendations.c.user_id == user_id).all()
    return games 

def add_game_to_blacklist(user_id, game_id):
    try:
        new_entry = UserBlacklist.insert().values(user_id=user_id, game_id=game_id)
        db.session.execute(new_entry)
        db.session.commit()
        print(f"Game {game_id} added to user {user_id}'s blacklist.")
        
    except Exception as e:
        db.session.rollback()
        print("Failed to add game: " + str(e))
        
def remove_game_from_blacklist(user_id, game_id):
    try:
        entry_to_delete = UserBlacklist.delete().where(UserBlacklist.c.user_id == user_id, UserBlacklist.c.game_id == game_id)
        db.session.execute(entry_to_delete)
        db.session.commit()
        print(f"Game {game_id} removed from user {user_id}'s blacklist.")
        
    except Exception as e:
        db.session.rollback()
        print("Failed to remove game: " + str(e))
        
def get_blacklist(user_id):
    games = db.session.query(Game).join(UserBlacklist).filter(UserBlacklist.c.user_id == user_id).all()
    return games 

def get_game_ratings(game_id):
    ratings = db.session.query(UserLibrary.c.rating).filter(UserLibrary.c.game_id == game_id).all()
    return [r[0] for r in ratings]