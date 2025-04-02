import pytest

def test_add_game_to_library_not_logged_in(client):
    # Test adding a game to the library without logging in
    response = client.post("/addgametolibrary", json={"title": "Some Game", "username": "John Not Doe", "password": "JohnDoePass"})
    assert response.status_code == 401
    assert response.json == {'error': 'User not logged in'}

def test_add_game_to_library_game_not_found(client):
    # Test adding a game that does not exist
    response = client.post("/addgametolibrary", json={"title": "Nonexistent Game", "username": "John Doe", "password": "JohnDoePass"})
    assert response.status_code == 404
    assert response.json == {'error': 'Game not found'}
    
def test_add_game_to_library_success(client):
    # Test adding a game to the library successfully
    response = client.post("/addgametolibrary", json={"title": "game1", "username": "John Doe", "password": "JohnDoePass"})
    assert response.status_code == 200
    assert response.json == {'success': 'Game added to library'}
    
    library = client.get("/getlibrary", query_string={"username": "John Doe"})
    assert library.status_code == 200
    assert len(library.json) == 1  # Expecting one game in the library

def test_get_library_bad_request(client):
    # Test getting the library with no username provided
    response = client.get("/getlibrary")
    assert response.status_code == 400
    assert response.json == {'error': 'Bad request'}

def test_get_library_success(client):
    # Test getting the library for a valid user
    response = client.get("/getlibrary", query_string={"username": "John Doe"})
    assert response.status_code == 200
    assert isinstance(response.json, list)  # Expecting a list of games

def test_remove_game_from_library_not_logged_in(client):
    # Test removing a game from the library without logging in
    response = client.post("/removegamefromlibrary", json={"title": "Some Game", "username": "John Not Doe", "password": "JohnDoePass"})
    assert response.status_code == 401
    assert response.json == {'error': 'User not logged in'}

def test_remove_game_from_library_game_not_found(client):
    # Test removing a game that does not exist
    response = client.post("/removegamefromlibrary", json={"title": "Nonexistent Game", "username": "John Doe", "password": "JohnDoePass"})
    assert response.status_code == 404
    assert response.json == {'error': 'Game not found'}
    
def test_remove_game_from_library_success(client):
    # Test removing a game from the library successfully
    add = client.post("/addgametolibrary", json={"title": "game1", "username": "John Doe", "password": "JohnDoePass"})
    assert add.status_code == 200
    
    response = client.post("/removegamefromlibrary", json={"title": "game1", "username": "John Doe", "password": "JohnDoePass"})
    assert response.status_code == 200
    assert response.json == {'success': 'Game removed from library'}
    
    library = client.get("/getlibrary", query_string={"username": "John Doe"})
    assert library.status_code == 200
    assert len(library.json) == 0  # Expecting no games in the library

def test_update_rating_not_logged_in(client):
    # Test updating a game's rating without logging in
    response = client.post("/updaterating", json={"title": "Some Game", "rating": 5, "username": "John Not Doe", "password": "JohnDoePass"})
    assert response.status_code == 401
    assert response.json == {'error': 'User not logged in'}

def test_update_rating_game_not_found(client):
    # Test updating the rating of a game that does not exist
    response = client.post("/updaterating", json={"title": "Nonexistent Game", "rating": 5, "username": "John Doe", "password": "JohnDoePass"})
    assert response.status_code == 404
    assert response.json == {'error': 'Game not found'}

def test_update_state_not_logged_in(client):
    # Test updating a game's state without logging in
    response = client.post("/updatestate", json={"title": "Some Game", "state": "Completed", "username": "John Not Doe", "password": "JohnDoePass"})
    assert response.status_code == 401
    assert response.json == {'error': 'User not logged in'}

def test_update_state_success(client):
    add = client.post("/addgametolibrary", json={"title": "game1", "username": "John Doe", "password": "JohnDoePass"})
    assert add.status_code == 200
    
    # Test updating the state of a game successfully
    response = client.post("/updatestate", json={"title": "game1", "state": "Completed", "username": "John Doe", "password": "JohnDoePass"})
    assert response.status_code == 200
    assert response.json == {'success': 'State updated'}
    
def test_update_rating_success(client):
    add = client.post("/addgametolibrary", json={"title": "game1", "username": "John Doe", "password": "JohnDoePass"})
    assert add.status_code == 200
    
    # Test updating the rating of a game successfully
    response = client.post("/updaterating", json={"title": "game1", "rating": 8, "username": "John Doe", "password": "JohnDoePass"})
    assert response.status_code == 200
    assert response.json == {'success': 'Rating updated'}

def test_update_state_game_not_found(client):
    # Test updating the state of a game that does not exist
    response = client.post("/updatestate", json={"title": "Nonexistent Game", "state": "Completed", "username": "John Doe", "password": "JohnDoePass"})
    assert response.json == {'error': 'Game not found'}

def test_game_ratings_game_not_found(client):
    # Test retrieving ratings for a game that does not exist
    response = client.get("/gameratings", query_string={"title": "Nonexistent Game"})
    assert response.status_code == 404
    assert response.json == {'error': 'Game not found'}

def test_game_ratings_success(client):
    # Test retrieving ratings for an existing game
    response = client.get("/gameratings", query_string={"title": "game1"})
    assert response.status_code == 200
    assert isinstance(response.json, list)  # Expecting a list of ratings