from flaskr import *


games = Blueprint("games", __name__)

@games.route('/getrecommendations', methods=['POST'])
def getrecommendations():
    data = request.get_json()
    
    user = log_user_in(data.get('username'), data.get('password'), session)
    if not user:
        return jsonify({'error':'User not logged in'}), 401
    
    games = get_recommendations(session['id'])
    response = [{'title': game.title, 'data': eval(game.data)} for game in games]
    return jsonify(response)

@games.route('/getlibrary', methods=['POST'])
def getlibary():
    data = request.get_json()
    
    user = log_user_in(data.get('username'), data.get('password'), session)
    if not user:
        return jsonify({'error':'User not logged in'}), 401
    
    items = get_libary(session['id'])
    response = [{'title': game.title, 'data': eval(game.data), 'rating': rating, 'state': state} for game, rating, state in items]
    return jsonify(response)
