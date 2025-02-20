from flask import Flask, jsonify, request, session
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from database import db, User, remove_user, create_user, login
from gemini import GenAI
from giantbomb import search_game
import os
from datetime import date

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
app.secret_key = os.getenv('SECRET_KEY')
db.init_app(app)

with app.app_context():
    db.create_all()
    
@app.route('/genai/', methods=['GET', 'POST'])
def promptAI():
    if session.get('username') is None:
        return [], 401
    
    prompt = request.args.get('prompt', 'Failed to send')
    response = GenAI.send_message(prompt)
    response = eval(response)
    
    for command in response:
        task = command.get("command", "")
        message = command.get("message", "")
        
        if task == "Recommend":
            pass
        elif task == "Add":
            pass
        elif task == "Remove":
            pass
        elif task == "Rate":
            pass
        elif task == "State":
            pass
    
    return jsonify(message), 200


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port='5000')