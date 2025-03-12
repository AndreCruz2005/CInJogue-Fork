from flask import Blueprint, request, session, jsonify
from database import *
from datetime import date

usersroute = Blueprint("users", __name__)

@usersroute.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()

    username = data.get('username')
    password = data.get('password')
    email = data.get('email')
    birthdate = data.get('birthdate')
    b = [int(n) for n in birthdate.split('-')]

    if not (username and password and email and birthdate):
        return jsonify({"error": "Missing required fields"}), 400

    if create_user(username, password, email, date(b[0], b[1], b[2])) is not None:
        return jsonify({"message": "User signed up successfully!"}), 201

    return jsonify({"error": "There was an error signing up!"}), 400

@usersroute.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    
    username = data.get('username')
    password = data.get('password')
    result = log_user_in(username, password, session)
    
    if result:
        return jsonify(get_user_by_name(result['username'])), 200
    else:
        return jsonify({"error":"Failed to Login"}), 401

@usersroute.route('/removeuser', methods=['POST'])
def removeuser():
    data = request.get_json()
    
    user = log_user_in(data.get('username'), data.get('password'), session)
    if not user:
        return jsonify({'error':'User not logged in'}), 401
    
    result = remove_user(session['id'])
    return jsonify(result), (200 if result else 500)


@usersroute.route('/changepassword', methods=['POST'])
def changepassword():
    data = request.get_json()
    
    user = log_user_in(data.get('username'), data.get('oldPassword'), session)
    if not user:
        return jsonify({'error':'User not logged in'}), 401
    
    result = change_password(session['id'], data.get('newPassword'))
    return jsonify(result), (200 if result else 500)


    
    
    
        
