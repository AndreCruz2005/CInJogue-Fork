import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from config import Config


db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
jwt = JWTManager()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.config['JWT_SECRET_KEY'] = os.getenv("JWT_SECRET_KEY")

    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    jwt.init_app(app)

    from app.routes.auth_routes import auth_bp
    from app.routes.game_routes import game_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(game_bp, url_prefix='/api/games')

    return app
