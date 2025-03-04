from flask import Blueprint, request, session, jsonify
from database import *

games = Blueprint("games", __name__)

@games.route('/getrecommendations', methods=['POST'])
def getrecommendations():
    data = request.get_json()
    
    user = log_user_in(data.get('username'), data.get('password'), session)
    if not user:
        return jsonify({'error':'User not logged in'}), 401
    
    games = get_recommendations(session['id'])
    response = { game.title:{ 'data': eval(game.data)} for game in games}
    return jsonify(response)

@games.route('/getlibrary', methods=['POST'])
def getlibary():
    data = request.get_json()
    
    user = log_user_in(data.get('username'), data.get('password'), session)
    if not user:
        return jsonify({'error':'User not logged in'}), 401
    
    items = get_libary(session['id'])
    response = {game.title:{'data': eval(game.data), 'rating': rating, 'state': state} for game, rating, state in items}
    return jsonify(response)

@games.route('/removegamefromlibrary', methods=['POST'])
def removegamefromlibrary():
    data = request.get_json()
    
    user = log_user_in(data.get('username'), data.get('password'), session)
    if not user:
        return jsonify({'error':'User not logged in'}), 401
    
    game = get_game_by_name(data.get('title'))
    if not game:
        return jsonify({'error':'Game not found'}), 404
    
    remove_game_from_library(session['id'], game['id'])
    return jsonify({'success':'Game removed from library'})

@games.route('/removegamefromrecommendations', methods=['POST'])
def removegamefromrecommendations():
    data = request.get_json()
    
    user = log_user_in(data.get('username'), data.get('password'), session)
    if not user:
        return jsonify({'error':'User not logged in'}), 401
    
    game = get_game_by_name(data.get('title'))
    if not game:
        return jsonify({'error':'Game not found'}), 404
    
    remove_game_from_recommendations(session['id'], game['id'])
    return jsonify({'success':'Game removed from recommendations'})

@games.route('/updaterating', methods=['POST'])
def updaterating():
    data = request.get_json()
    
    user = log_user_in(data.get('username'), data.get('password'), session)
    if not user:
        return jsonify({'error':'User not logged in'}), 401
    
    game = get_game_by_name(data.get('title'))
    if not game:
        return jsonify({'error':'Game not found'}), 404
    
    update_game_rating(session['id'], game['id'], data.get('rating'))
    return jsonify({'success':'Rating updated'})

@games.route('/updatestate', methods=['POST'])
def updatestate():
    data = request.get_json()
    
    user = log_user_in(data.get('username'), data.get('password'), session)
    if not user:
        return jsonify({'error':'User not logged in'}), 401
    
    game = get_game_by_name(data.get('title'))
    if not game:
        return jsonify({'error':'Game not found'}), 404
    
    update_game_state(session['id'], game['id'], data.get('state'))
    return jsonify({'success':'State updated'})

@games.route('/blacklistgame', methods=['POST'])
def blacklistgame():
    data = request.get_json()
    
    user = log_user_in(data.get('username'), data.get('password'), session)
    if not user:
        return jsonify({'error':'User not logged in'}), 401
    
    game = get_game_by_name(data.get('title'))
    if not game:
        return jsonify({'error':'Game not found'}), 404
    
    add_game_to_blacklist(session['id'], game['id'])
    return jsonify({'success':'Game blacklisted'})

@games.route('/unblacklistgame', methods=['POST'])
def unblacklistgame():
    data = request.get_json()
    
    user = log_user_in(data.get('username'), data.get('password'), session)
    if not user:
        return jsonify({'error':'User not logged in'}), 401
    
    game = get_game_by_name(data.get('title'))
    if not game:
        return jsonify({'error':'Game not found'}), 404
    
    remove_game_from_blacklist(session['id'], game['id'])
    return jsonify({'success':'Game unblacklisted'})

@games.route('/addgametolibrary', methods=['POST'])
def addgametolibrary():
    data = request.get_json()
    
    user = log_user_in(data.get('username'), data.get('password'), session)
    if not user:
        return jsonify({'error':'User not logged in'}), 401
    
    game = get_game_by_name(data.get('title'))
    if not game:
        return jsonify({'error':'Game not found'}), 404
    
    add_game_to_library(session['id'], game['id'])
    return jsonify({'success':'Game added to library'})

@games.route('/gameratings', methods=['GET'])
def gameratings():
    title = request.args.get('title', '')
    game = get_game_by_name(title)
    if not game:
        return jsonify({'error':'Game not found'}), 404
    
    return jsonify(get_game_ratings(game['id']))

@games.route('/getblacklist', methods=['POST'])
def getblacklist():
    data = request.get_json()
    
    user = log_user_in(data.get('username'), data.get('password'), session)
    if not user:
        return jsonify({'error':'User not logged in'}), 401
    
    items = get_blacklist(session['id'])
    response = [game.title for game in items]
    return jsonify(response)