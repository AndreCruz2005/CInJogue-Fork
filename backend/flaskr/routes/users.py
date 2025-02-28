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
        return jsonify(get_user_by_name(result['username']))
    else:
        return jsonify({"error":"Failed to Login"})


@users.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({"message":"User logged out succesfully"})

@users.route('/removeuser', methods=['POST'])
def remove_user():
    if session.get('username') is None:
        return {"error": "User is not logged in!"}
    
    password = request.json.get('password')  
    if check_password_hash(session['password'], password):
        remove_user(session['username'])
        session.clear()
        return {"message": "User deleted successfully!"}

    return {"error": "Incorrect password!"}

@users.route('/loggedinuser', methods=['GET'])
def loggedinuser():
    name = session.get('username')
    if name:
        return jsonify(get_user_by_name(name))
    return jsonify({'error':'User not logged in'})
