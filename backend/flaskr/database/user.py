from database.database import db
from werkzeug.security import generate_password_hash, check_password_hash

UserLibrary = db.Table(
    'user_library',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('game_id', db.Integer, db.ForeignKey('game.id'), primary_key=True),
    db.Column('rating', db.Integer),
    db.Column('state', db.String)
)

UserRecommendations = db.Table(
    'user_recommendations',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('game_id', db.Integer, db.ForeignKey('game.id'), primary_key=True)
)

UserBlacklist = db.Table(
    'user_blacklist',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('game_id', db.Integer, db.ForeignKey('game.id'), primary_key=True)
)

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    birthdate = db.Column(db.Date(), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)
    library = db.relationship('Game', secondary=UserLibrary, backref='library_users')
    recommendations = db.relationship('Game', secondary=UserRecommendations, backref='recommendations_users')
    blacklist = db.relationship('Game', secondary=UserBlacklist, backref='blacklist_users')
    
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