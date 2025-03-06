from flask import Blueprint, request, session, jsonify
from database import *
from datetime import date

users = Blueprint("users", __name__)

@users.route('/signup', methods=['POST'])
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

@users.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    
    username = data.get('username')
    password = data.get('password')
    result = log_user_in(username, password, session)
    
    if result:
        return jsonify(get_user_by_name(result['username'])), 200
    else:
        return jsonify({"error":"Failed to Login"}), 401


@users.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({"message":"User logged out succesfully"})

@users.route('/removeuser', methods=['POST'])
def removeuser():
    data = request.get_json()
    
    user = log_user_in(data.get('username'), data.get('password'), session)
    if not user:
        return jsonify({'error':'User not logged in'}), 401
    
    result = remove_user(session['id'])
    return jsonify(result), (200 if result else 500)


@users.route('/loggedinuser', methods=['GET'])
def loggedinuser():
    name = session.get('username')
    if name:
        return jsonify(get_user_by_name(name))
    return jsonify({'error':'User not logged in'})

@users.route('/changepassword', methods=['POST'])
def changepassword():
    data = request.get_json()
    
    user = log_user_in(data.get('username'), data.get('oldPassword'), session)
    if not user:
        return jsonify({'error':'User not logged in'}), 401
    
    result = change_password(session['id'], data.get('newPassword'))
    return jsonify(result), (200 if result else 500)

@users.route('/addtags', methods=['POST'])
def addtags():
    data = request.get_json()
    
    user = log_user_in(data.get('username'), data.get('password'), session)
    if not user:
        return jsonify({'error':'User not logged in'}), 401
    
    response = add_user_tag(session['id'], data.get('text'), data.get('tag_type'))
    return jsonify(response), 200

@users.route('/removetags', methods=['POST'])
def removetags():
    data = request.get_json()
    
    user = log_user_in(data.get('username'), data.get('password'), session)
    if not user:
        return jsonify({'error':'User not logged in'}), 401
    
    response = remove_user_tag(session['id'], data.get('text'))
    return jsonify(response), 200

@users.route('/gettags', methods=['POST'])
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
    
    
    
        
