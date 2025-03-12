from flask import Blueprint, request, session, jsonify
from database import *

tagsroute = Blueprint("tags", __name__)

@tagsroute.route('/addtags', methods=['POST'])
def addtags():
    data = request.get_json()
    
    user = log_user_in(data.get('username'), data.get('password'), session)
    if not user:
        return jsonify({'error':'User not logged in'}), 401
    
    response = add_user_tag(session['id'], data.get('text'), data.get('tag_type'))
    return jsonify(response), (201 if response else 500)

@tagsroute.route('/removetags', methods=['POST'])
def removetags():
    data = request.get_json()
    
    user = log_user_in(data.get('username'), data.get('password'), session)
    if not user:
        return jsonify({'error':'User not logged in'}), 401
    
    response = remove_user_tag(session['id'], data.get('text'))
    return jsonify(response), (200 if response else 500)

@tagsroute.route('/gettags', methods=['POST'])
def gettags():
    data = request.get_json()
    
    user = log_user_in(data.get('username'), data.get('password'), session)
    if not user:
        return jsonify({'error':'User not logged in'}), 401
    
    tags = get_tags(session['id'])
    
    # Cria um dicionário com as tags listadas e associadas ao seus respectivos tipos
    response = {}
    for tag in tags:
        if tag[3] not in response:
            response[tag[3]] = []

        response[tag[3]].append(tag[2])
    return jsonify(response), 200
