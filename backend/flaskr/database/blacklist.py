from database.database import db

UserBlacklist = db.Table(
    'user_blacklist',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('game_id', db.Integer, db.ForeignKey('game.id'), primary_key=True),
)

from database.game import *
from database.user import *

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