from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models import Game
from app.services.giant_bomb_service import search_game_on_giant_bomb


game_bp = Blueprint('games', __name__)

@game_bp.route('/search', methods=['GET'])
@jwt_required()
def search_game():
    query = request.args.get('query')
    results = search_game_on_giant_bomb(query)
    return jsonify(results), 200

@game_bp.route('/add', methods=['POST'])
@jwt_required()
def add_game():
    data = request.get_json()
    user_id = get_jwt_identity()
    new_game = Game(user_id=user_id, name=data['name'], image=data.get('image'))
    db.session.add(new_game)
    db.session.commit()
    return jsonify({'message': 'Game added to your library'}), 201

@game_bp.route('/list', methods=['GET'])
@jwt_required()
def list_games():
    user_id = get_jwt_identity()
    games = Game.query.filter_by(user_id=user_id).all()
    
    games_list = [
        {
            'id': game.id,
            'name': game.name,
            'image': game.image,
            'created_at': game.created_at
        }
        for game in games
    ]
    
    return jsonify(games_list), 200

