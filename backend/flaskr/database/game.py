from database.database import db

class Game(db.Model):
    __tablename__ = "game"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False, unique=True)
    data = db.Column(db.Text())

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
    
def get_game_by_name(title):
    game = db.session.query(Game).filter_by(title=title).first()
    if game:
        return {
            "id": game.id,
            "title": game.title,
            "data": game.data
        }
    return None
