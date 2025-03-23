from database.database import db

UserLibrary = db.Table(
    'user_library',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('game_id', db.Integer, db.ForeignKey('game.id'), primary_key=True),
    db.Column('rating', db.Integer),
    db.Column('state', db.String)
)

from database.game import *
from database.user import * 

def add_game_to_library(user_id, game_id):
    try:
        new_entry = UserLibrary.insert().values(user_id=user_id, game_id=game_id, rating=0, state='NÃO JOGADO')
        db.session.execute(new_entry)
        db.session.commit()
        print(f"Game {game_id} added to user {user_id}'s library.")
        
    except Exception as e:
        db.session.rollback()
        print("Failed to add game to library: " + str(e))
        
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

def get_game_ratings(game_id):
    ratings = db.session.query(UserLibrary.c.rating).filter(UserLibrary.c.game_id == game_id).all()
    return [r[0] for r in ratings]
    