from flask import Blueprint, request, session, jsonify
from database import *

blacklistroute = Blueprint("blacklistroute", __name__)

@blacklistroute.route('/blacklistgame', methods=['POST'])
def blacklistgame():
    data = request.get_json()
    
    user = log_user_in(data.get('username'), data.get('password'), session)
    if not user:
        return jsonify({'error':'User not logged in'}), 401
    
    game = get_game_by_name(data.get('title'))
    if not game:
        return jsonify({'error':'Game not found'}), 404
    
    add_game_to_blacklist(session['id'], game['id'])
    return jsonify({'success':'Game blacklisted'}), 200

@blacklistroute.route('/unblacklistgame', methods=['POST'])
def unblacklistgame():
    data = request.get_json()
    
    user = log_user_in(data.get('username'), data.get('password'), session)
    if not user:
        return jsonify({'error':'User not logged in'}), 401
    
    game = get_game_by_name(data.get('title'))
    if not game:
        return jsonify({'error':'Game not found'}), 404
    
    remove_game_from_blacklist(session['id'], game['id'])
    return jsonify({'success':'Game unblacklisted'}), 200

@blacklistroute.route('/getblacklist', methods=['POST'])
def getblacklist():
    data = request.get_json()
    
    user = log_user_in(data.get('username'), data.get('password'), session)
    if not user:
        return jsonify({'error':'User not logged in'}), 401
    
    items = get_blacklist(session['id'])
    response = [game.title for game in items]
    return jsonify(response), 200