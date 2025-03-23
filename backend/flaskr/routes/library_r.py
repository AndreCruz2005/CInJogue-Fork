from flask import Blueprint, request, session, jsonify
from database import *

libraryroute = Blueprint("libraryroute", __name__)

@libraryroute.route('/addgametolibrary', methods=['POST'])
def addgametolibrary():
    data = request.get_json()
    
    user = log_user_in(data.get('username'), data.get('password'), session)
    if not user:
        return jsonify({'error':'User not logged in'}), 401
    
    game = get_game_by_name(data.get('title'))
    if not game:
        return jsonify({'error':'Game not found'}), 404
    
    add_game_to_library(session['id'], game['id'])
    return jsonify({'success':'Game added to library'}), 200

@libraryroute.route('/getlibrary', methods=['GET'])
def getlibary():
    data = request.args.get("username")
    
    if not data:
        return jsonify({'error':'Bad request'}), 400
    
    u = get_user_by_name(data)
    items = get_libary(u['id'])
    response = [{'title':game.title, 'data': eval(game.data), 'rating': rating, 'state': state} for game, rating, state in items]
    return jsonify(response), 200

@libraryroute.route('/removegamefromlibrary', methods=['POST'])
def removegamefromlibrary():
    data = request.get_json()
    
    user = log_user_in(data.get('username'), data.get('password'), session)
    if not user:
        return jsonify({'error':'User not logged in'}), 401
    
    game = get_game_by_name(data.get('title'))
    if not game:
        return jsonify({'error':'Game not found'}), 404
    
    remove_game_from_library(session['id'], game['id'])
    return jsonify({'success':'Game removed from library'}), 200

@libraryroute.route('/updaterating', methods=['POST'])
def updaterating():
    data = request.get_json()
    
    user = log_user_in(data.get('username'), data.get('password'), session)
    if not user:
        return jsonify({'error':'User not logged in'}), 401
    
    game = get_game_by_name(data.get('title'))
    if not game:
        return jsonify({'error':'Game not found'}), 404
    
    update_game_rating(session['id'], game['id'], data.get('rating'))
    return jsonify({'success':'Rating updated'}), 200

@libraryroute.route('/updatestate', methods=['POST'])
def updatestate():
    data = request.get_json()
    
    user = log_user_in(data.get('username'), data.get('password'), session)
    if not user:
        return jsonify({'error':'User not logged in'}), 401
    
    game = get_game_by_name(data.get('title'))
    if not game:
        return jsonify({'error':'Game not found'}), 404
    
    update_game_state(session['id'], game['id'], data.get('state'))
    return jsonify({'success':'State updated'}), 200

@libraryroute.route('/gameratings', methods=['GET'])
def gameratings():
    title = request.args.get('title', '')
    game = get_game_by_name(title)
    if not game:
        return jsonify({'error':'Game not found'}), 404
    
    return jsonify(get_game_ratings(game['id'])), 200