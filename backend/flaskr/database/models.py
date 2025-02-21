from database.database import db

UserLibary = db.Table(
    'user_library',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('game_id', db.Integer, db.ForeignKey('game.id'), primary_key=True)
)

UserRecommendations = db.Table(
    'user_recommendations',
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
    library = db.relationship('Game', secondary=UserLibary, backref='library_users')
    recommendations = db.relationship('Game', secondary=UserRecommendations, backref='recommendations_users')

class Game(db.Model):
    __tablename__ = "game"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False, unique=True)
    rating = db.Column(db.Integer(), nullable=False)
    state = db.Column(db.String(255), nullable=False)
    data = db.Column(db.Text())
