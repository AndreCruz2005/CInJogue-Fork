from flask import Flask, jsonify, request, session
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from database import *
from gemini import GenAI
from giantbomb import search_game
from datetime import date
import os

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}}, supports_credentials=True)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
app.secret_key = os.getenv('SECRET_KEY')
db.init_app(app)

with app.app_context():
    db.create_all()


@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()

    username = data.get('username')
    password = data.get('password')
    email = data.get('email')
    birthdate = data.get('birthdate')
    b = [int(n) for n in birthdate.split('-')]

    if not (username and password and email and birthdate):
        return jsonify({"error": "Missing required fields"}), 400

    if create_user(username, password, email, date(b[0], b[1], b[2]))is not None:
        return jsonify({"message": "User signed up successfully!"}), 201

    return jsonify({"error": "There was an error signing up!"}), 400

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    
    username = data.get('username')
    password = data.get('password')
    result = log_user_in(username, password, session)
    
    if result:
        return jsonify(get_user_by_name(result['username']))
    else:
        return jsonify({"error":"Failed to Login"})


@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({"message":"User logged out succesfully"})

@app.route('/removeuser', methods=['POST'])
def remove_user():
    if session.get('username') is None:
        return {"error": "User is not logged in!"}
    
    password = request.json.get('password')  
    if check_password_hash(session['password'], password):
        remove_user(session['username'])
        session.clear()
        return {"message": "User deleted successfully!"}

    return {"error": "Incorrect password!"}

@app.route('/loggedinuser', methods=['GET'])
def loggedinuser():
    name = session.get('username')
    if name:
        return jsonify(get_user_by_name(name))
    return jsonify({'error':'User not logged in'})

@app.route('/getrecommendations', methods=['POST'])
def getrecommendations():
    data = request.get_json()
    
    user = log_user_in(data.get('username'), data.get('password'), session)
    if not user:
        return jsonify({'error':'User not logged in'}), 401
    
    games = get_recommendations(session['id'])
    response = [{'title': game.title, 'data': eval(game.data)} for game in games]
    return jsonify(response)

@app.route('/getlibrary', methods=['POST'])
def getlibary():
    data = request.get_json()
    
    user = log_user_in(data.get('username'), data.get('password'), session)
    if not user:
        return jsonify({'error':'User not logged in'}), 401
    
    items = get_libary(session['id'])
    response = [{'title': game.title, 'data': eval(game.data), 'rating': rating, 'state': state} for game, rating, state in items]
    return jsonify(response)

@app.route('/genai', methods=['POST'])
def promptAI():
    data = request.get_json()
    
    user = log_user_in(data.get('username'), data.get('password'), session)
    if not user:
        return jsonify({'error':'User not logged in'}), 401
    
    prompt = data.get('prompt')
    response = GenAI.send_message(prompt)
    response = eval(response)
    
    for task in response:
        command = task.get("command", "")
        titles = task.get("titles", [])
        other = task.get("other", [])
        
        if command == "Recommend":
            for title in titles:
                game = ensureGameExistence(title)
                if game and session.get('id'):
                    add_game_to_recommendations(session['id'], game)

        elif command == "Add":
            for title in titles:
                game = ensureGameExistence(title)
                if game and session.get('id'):
                    add_game_to_library(session['id'], game)
                    
        elif command == "Remove":
            for title in titles:
                game = db.session.query(Game).filter_by(title=title).first()
                if game and session.get('id'):
                    remove_game_from_library(session['id'], game.id)

        elif command == "Rate":
            for title, rating in zip(titles, other):
                game = db.session.query(Game).filter_by(title=title).first()
                if game and session.get('id'):
                    update_game_rating(session['id'], game.id, rating)
                
        elif command == "State":
            for title, state in zip(titles, other):
                game = db.session.query(Game).filter_by(title=title).first()
                if game and session.get('id'):
                    update_game_state(session['id'], game.id, state)
    
    return jsonify(response), 200

def ensureGameExistence(title: str) -> Game:
    game = db.session.query(Game).filter_by(title=title).first()
    
    if not game:
        game_results = search_game(title)
        
        if game_results:
            for i, result in enumerate(game_results):
                game_name = title if i == 0 else result['name']
                create_game(title=game_name, data=str(result))
            
            db.session.commit() 
 
            game = db.session.query(Game).filter_by(title=title).first()
    
    return game
    
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port='5000', threaded=True)