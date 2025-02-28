from database.database import db

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

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    birthdate = db.Column(db.Date(), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)
    library = db.relationship('Game', secondary=UserLibrary, backref='library_users')
    recommendations = db.relationship('Game', secondary=UserRecommendations, backref='recommendations_users')

class Game(db.Model):
    __tablename__ = "game"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False, unique=True)
    data = db.Column(db.Text())
