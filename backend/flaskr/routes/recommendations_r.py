from flask import Blueprint, request, session, jsonify
from database import *

recommendationsroute = Blueprint("recommendations", __name__)

@recommendationsroute.route('/getrecommendations', methods=['POST'])
def getrecommendations():
    data = request.get_json()
    
    user = log_user_in(data.get('username'), data.get('password'), session)
    if not user:
        return jsonify({'error':'User not logged in'}), 401
    
    games = get_recommendations(session['id'])
    response = [{'title':game.title, 'data': eval(game.data)} for game in games]
    return jsonify(response)

@recommendationsroute.route('/removegamefromrecommendations', methods=['POST'])
def removegamefromrecommendations():
    data = request.get_json()
    
    user = log_user_in(data.get('username'), data.get('password'), session)
    if not user:
        return jsonify({'error':'User not logged in'}), 401
    
    game = get_game_by_name(data.get('title'))
    if not game:
        return jsonify({'error':'Game not found'}), 404
    
    remove_game_from_recommendations(session['id'], game['id'])
    return jsonify({'success':'Game removed from recommendations'}), 200