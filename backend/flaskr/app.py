from flask import Flask, jsonify
from flask_cors import CORS
from flask_migrate import Migrate
from database import *
from routes import airoute, blacklistroute, libraryroute, recommendationsroute, tagsroute, usersroute
import os

def create_app(database_uri=os.getenv('SQLALCHEMY_DATABASE_URI')):
    app = Flask(__name__)
    migrate = Migrate(app, db, "database/migrations")
    app.register_blueprint(airoute)
    app.register_blueprint(blacklistroute)
    app.register_blueprint(libraryroute)
    app.register_blueprint(recommendationsroute)
    app.register_blueprint(tagsroute)
    app.register_blueprint(usersroute)

    CORS(app)

    app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
    app.secret_key = os.getenv('SECRET_KEY')
    db.init_app(app)

    with app.app_context():
        db.create_all()
        
    @app.route("/")
    def check():
        return jsonify("CInJogue online e operacional!"), 200
    
    return app

if __name__ == "__main__":
    create_app().run(debug=True, host='0.0.0.0', port=os.getenv('BACKEND_PORT'), threaded=True)