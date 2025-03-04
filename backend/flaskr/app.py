from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from database import db
from routes import users, games, gai
import os

app = Flask(__name__)
migrate = Migrate(app, db)
app.register_blueprint(users)
app.register_blueprint(games)
app.register_blueprint(gai)

CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
app.secret_key = os.getenv('SECRET_KEY')
db.init_app(app)

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port='5000', threaded=True)