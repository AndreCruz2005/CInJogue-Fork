from flask import Flask, jsonify, request, session
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from database import db, User, Game, remove_user, create_user, login, get_user_by_name, create_game, add_game_to_recommendations, add_game_to_library, remove_game_from_library
from gemini import GenAI
from giantbomb import search_game
from datetime import date
import os

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
app.secret_key = os.getenv('SECRET_KEY')
db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/signup/', methods=['GET', 'POST'])
def r_signup():
    username = request.args.get('username')
    password = request.args.get('password')
    email = request.args.get("email")
    birthdate = request.args.get("birthdate")
    b = [int(n) for n in birthdate.split('-')]
    
    if create_user(username, password, email, date(b[0], b[1], b[2]))is not None:
        login(username, password, session)
        return jsonify(True)
      
    return jsonify(False)

@app.route('/logout', methods=['POST'])
def r_logout():
    session.clear()
    return jsonify(True)

@app.route('/removeuser',  methods=['GET', 'POST'])
def r_remove_user():
    if session.get('username') is None:
        return jsonify(False)
    
    password = request.args.get('password')
    if check_password_hash(session['password'], password):
        remove_user(session['username'])
        session.clear()
        return jsonify(True)

    return jsonify(False)

@app.route('/loggedinuser', methods=['GET'])
def loggedinuser():
    name = session.get('username')
    if name:
        return jsonify(get_user_by_name(name))
    return jsonify({})

@app.route('/login/', methods=['GET', 'POST'])
def r_login():
    username = request.args.get('username')
    password = request.args.get('password')
    result = login(username, password, session)
    return jsonify(result)

@app.route('/genai/', methods=['GET', 'POST'])
def promptAI():
    if session.get('username') is None:
        return [], 401
    
    prompt = request.args.get('prompt', 'Failed to send')
    response = GenAI.send_message(prompt)
    response = eval(response)
    
    for task in response:
        command = task.get("command", "")
        message = task.get("message", "")
        titles = task.get("titles", [])
        other = task.get("other", [])
        
        if command == "Recommend":
            for title in titles:
                game = db.session.query(Game).filter_by(title=title).first()
                if not game:
                    game_results = search_game(title)
                    for game in game_results:
                        create_game(title=game['name'], data=str(game))
                    game = db.session.query(Game).filter_by(title=title).first()
                
                if game and session.get('id'):
                    add_game_to_recommendations(session['id'], game.id)

        elif command == "Add":
            for title in titles:
                game = db.session.query(Game).filter_by(title=title).first()
                if not game:
                    game_results = search_game(title)
                    for game in game_results:
                        create_game(title=game['name'], data=str(game))
                    game = db.session.query(Game).filter_by(title=title).first()
                
                if game and session.get('id'):
                    add_game_to_library(session['id'], game.id)
                    
        elif command == "Remove":
            for title in titles:
                game = db.session.query(Game).filter_by(title=title).first()
                if game and session.get('id'):
                    remove_game_from_library(session['id'], game.id)

        elif command == "Rate":
            pass
        elif command == "State":
            pass
    
    return jsonify(response), 200


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port='5000')