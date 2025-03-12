from database.database import db
from werkzeug.security import generate_password_hash, check_password_hash
from database.tags import remove_all_user_tags
from database.library import UserLibrary
from database.recommendations import UserRecommendations
from database.blacklist import UserBlacklist

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

def remove_user(user_id):
    try:
        user = db.session.query(User).filter_by(id=user_id).first()

        if user:
            remove_all_user_tags(user_id)
            db.session.delete(user)
            db.session.commit()
            return True  
        return False

    except Exception as e:
        db.session.rollback() 
        print(f"Error removing user: {e}")
        return False
    
def change_password(user_id, password):
    try:
        hashed_password = generate_password_hash(password)
        user = db.session.query(User).filter_by(id=user_id).first()
        
        if user:
            user.password = hashed_password
            db.session.commit()
            return True
        return False

    except Exception as e:
        db.session.rollback()
        print(f"Error changing password: {e}")
        return False
    
