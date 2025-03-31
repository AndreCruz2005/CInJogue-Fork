import pytest

def test_get_recommendations(client):
    # Log in with a test user
    response = client.post('/getrecommendations', json={"username": "John Doe", "password": "JohnDoePass"})
    assert response.status_code == 200

    # Check if the recommendations are returned
    recommendations = response.get_json()
    assert isinstance(recommendations, list)
    assert recommendations == []

def test_get_recommendations_unauthorized(client):
    # Attempt to get recommendations without valid credentials
    response = client.post('/getrecommendations', json={"username": "InvalidUser", "password": "InvalidPass"})
    assert response.status_code == 401
    assert response.get_json() == {'error': 'User not logged in'}

def test_remove_game_from_recommendations(client):
    # Log in with a test user
    response = client.post('/removegamefromrecommendations', json={"username": "John Doe", "password": "JohnDoePass", "title": "game1"})
    assert response.status_code == 200
    assert response.get_json() == {'success': 'Game removed from recommendations'}

def test_remove_game_from_recommendations_not_found(client):
    # Attempt to remove a game that does not exist
    response = client.post('/removegamefromrecommendations', json={"username": "John Doe", "password": "JohnDoePass", "title": "nonexistent_game"})
    assert response.status_code == 404
    assert response.get_json() == {'error': 'Game not found'}

def test_remove_game_from_recommendations_unauthorized(client):
    # Attempt to remove a game without valid credentials
    response = client.post('/removegamefromrecommendations', json={"username": "InvalidUser", "password": "InvalidPass", "title": "game1"})
    assert response.status_code == 401
    assert response.get_json() == {'error': 'User not logged in'}