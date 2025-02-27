from flaskr import *

gai = Blueprint("genai", __name__)

@gai.route('/genai', methods=['POST'])
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
    