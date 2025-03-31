def test_blacklistgame_user_not_logged_in(client):
    # Test calling with user not logged in
    response = client.post("/blacklistgame", json={"title": "Some Game"})
    assert response.json == {'error': 'User not logged in'}
    assert response.status_code == 401


def test_unblacklistgame_user_not_logged_in(client):
    # Test calling unblacklistgame with user not logged in
    response = client.post("/unblacklistgame", json={"title": "Some Game"})
    assert response.json == {'error': 'User not logged in'}
    assert response.status_code == 401

def test_getblacklist_user_not_logged_in(client):
    # Test calling getblacklist with user not logged in
    response = client.post("/getblacklist", json={})
    assert response.json == {'error': 'User not logged in'}
    assert response.status_code == 401

def test_blacklistgame_no_game(client):
    response = client.post("/blacklistgame", json={"title": "Some Game", "username": "John Doe", "password": "JohnDoePass"})
    assert response.status_code == 404
    assert response.json == {'error': 'Game not found'}
    
def test_unblacklistgame_no_game(client):
    response = client.post("/unblacklistgame", json={"title": "Some Game", "username": "John Doe", "password": "JohnDoePass"})
    assert response.status_code == 404
    assert response.json == {'error': 'Game not found'}
    
def test_getblacklist_no_game(client):
    response = client.post("/getblacklist", json={"username": "John Doe", "password": "JohnDoePass"})
    assert response.status_code == 200
    assert response.json == []
    
def test_blacklistgame(client):
    response = client.post("/blacklistgame", json={"title": "game1", "username": "John Doe", "password": "JohnDoePass"})
    assert response.status_code == 200
    assert response.json == {'success': 'Game blacklisted'}
    
    blacklist = client.post("/getblacklist", json={"username": "John Doe", "password": "JohnDoePass"})
    assert blacklist.status_code == 200
    assert len(blacklist.json) == 1
    assert blacklist.json[0] == "game1"
    
    # Unblacklist game
    unblacklist = client.post("/unblacklistgame", json={"title": "game1", "username": "John Doe", "password": "JohnDoePass"})
    assert unblacklist.status_code == 200
    assert unblacklist.json == {'success': 'Game unblacklisted'}
    
    blacklist = client.post("/getblacklist", json={"username": "John Doe", "password": "JohnDoePass"})
    assert blacklist.status_code == 200
    assert len(blacklist.json) == 0
    assert blacklist.json == []