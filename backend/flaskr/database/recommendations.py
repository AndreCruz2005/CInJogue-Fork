from database.database import db

UserRecommendations = db.Table(
    'user_recommendations',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('game_id', db.Integer, db.ForeignKey('game.id'), primary_key=True)
)

from database.game import *
from database.user import *

def add_game_to_recommendations(user_id, game):
    try:
        new_entry = UserRecommendations.insert().values(user_id=user_id, game_id=game.id)
        db.session.execute(new_entry)
        db.session.commit()
        print(f"Game {game.title} added to user {user_id}'s recommendations.")
        
    except Exception as e:
        db.session.rollback()
        print("Failed to add game: " + str(e))
        
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

def get_recommendations(user_id):
    games = db.session.query(Game).join(UserRecommendations).filter(UserRecommendations.c.user_id == user_id).all()
    return games 