from flask import Blueprint, request, session, jsonify
from gemini import GenAI
from giantbomb import search_game
from database import *
import os

airoute = Blueprint("airoute", __name__)

@airoute.route('/genai', methods=['POST'])
def promptAI():
    data = request.get_json()
    
    user = log_user_in(data.get('username'), data.get('password'), session)
    if not user:
        return jsonify({'error':'User not logged in'}), 401
    
    prompt = data.get('prompt')
    prompt = format_prompt(prompt)
    print(prompt)
    response = GenAI.send_message(str(prompt))
    response = eval(response)
    
    for task in response:
        command = task.get("command", "")
        titles = task.get("titles", [])
        other = task.get("other", [])
        
        if command == "Recommend":
            clear_user_recommendations(session['id'])
            for title in titles:
                game = ensure_game_existence(title)
                if game and session.get('id'):
                    add_game_to_recommendations(session['id'], game)

        elif command == "Add":
            for title in titles:
                game = ensure_game_existence(title)
                if game and session.get('id'):
                    add_game_to_library(session['id'], game.id)
                    
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

def ensure_game_existence(title: str) -> Game:
    game = db.session.query(Game).filter_by(title=title).first()
    
    if not game:
        game_results = search_game(title)
        
        if game_results:
            for i, result in enumerate(game_results):
                if i == 0:
                    game = create_game(title=result['name'], data=str(result))
                else:
                    create_game(title=result['name'], data=str(result))
            
            db.session.commit()     
    return game

def format_prompt(prompt: str) -> dict:
    libray = get_libary(session['id'])
    recommendations = get_recommendations(session['id'])
    userinfo ={k:v for k, v in get_user_by_name(session['username']).items() if k == 'username' or k == 'birthdate'} 
    blacklist = [game.title for game in get_blacklist(session['id'])]

    tags = get_tags(session['id'])
    preferences = {tag[3]:[] for tag in tags}
    for tag in tags:
        preferences[tag[3]].append(tag[2])
    
    return {
        "prompt": prompt, 
        "library": {game.title:{'rating': rating, 'state': state} for game, rating, state in libray}, 
        "recommendations": {game.title:{ 'title': game.title} for game in recommendations}, 
        "other": {'userinfo': userinfo, 'blacklist':blacklist, 'preferences':preferences}
        }
    
import speech_recognition as sr

@airoute.route('/uploadaudio', methods=['POST'])
def uploadaudio():
    recognizer = sr.Recognizer()
    
    if 'audio' not in request.files:
        return jsonify({"error": "No audio file provided"}), 400
    
    audio = request.files['audio']
    
    try:
        # Use the audio file directly without saving it
        with sr.AudioFile(audio) as source:
            audio_data = recognizer.record(source)
        
        string = recognizer.recognize_google(audio_data, language="pt-BR")
        print("Text: " + string)
        return jsonify(string), 200
    except Exception as e:
        print("Exception: " + str(e))
        return jsonify({"error": str(e)}), 500