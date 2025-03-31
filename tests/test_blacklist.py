from unittest.mock import patch

def test_blacklistgame_user_not_logged_in(client):
    # Test calling with user not logged in
    response = client.post("/blacklistgame", json={"title": "Some Game"})
    assert response.json == {'error': 'User not logged in'}
    assert response.status_code == 401

@patch("routes.blacklist_r.log_user_in", return_value={"id": 1})
@patch("routes.blacklist_r.get_game_by_name", return_value={"id": 2, "title": "Some Game"})
@patch("routes.blacklist_r.add_game_to_blacklist")
def test_blacklistgame_success(mock_add_game, mock_get_game, mock_log_user, client):
    # Test successful blacklisting of a game
    response = client.post("/blacklistgame", json={"username": "testuser", "password": "testpass", "title": "Some Game"})
    assert response.json == {'success': 'Game blacklisted'}
    assert response.status_code == 200
    mock_log_user.assert_called_once_with("testuser", "testpass", client.session_transaction())
    mock_get_game.assert_called_once_with("Some Game")
    mock_add_game.assert_called_once_with(1, 2)

@patch("routes.blacklist_r.log_user_in", return_value={"id": 1})
@patch("routes.blacklist_r.get_game_by_name", return_value=None)
def test_blacklistgame_game_not_found(mock_get_game, mock_log_user, client):
    # Test blacklisting a game that does not exist
    response = client.post("/blacklistgame", json={"username": "testuser", "password": "testpass", "title": "Nonexistent Game"})
    assert response.json == {'error': 'Game not found'}
    assert response.status_code == 404
    mock_log_user.assert_called_once_with("testuser", "testpass", client.session_transaction())
    mock_get_game.assert_called_once_with("Nonexistent Game")

def test_unblacklistgame_user_not_logged_in(client):
    # Test calling unblacklistgame with user not logged in
    response = client.post("/unblacklistgame", json={"title": "Some Game"})
    assert response.json == {'error': 'User not logged in'}
    assert response.status_code == 401

@patch("routes.blacklist_r.log_user_in", return_value={"id": 1})
@patch("routes.blacklist_r.get_game_by_name", return_value={"id": 2, "title": "Some Game"})
@patch("routes.blacklist_r.remove_game_from_blacklist")
def test_unblacklistgame_success(mock_remove_game, mock_get_game, mock_log_user, client):
    # Test successful unblacklisting of a game
    response = client.post("/unblacklistgame", json={"username": "testuser", "password": "testpass", "title": "Some Game"})
    assert response.json == {'success': 'Game unblacklisted'}
    assert response.status_code == 200
    mock_log_user.assert_called_once_with("testuser", "testpass", client.session_transaction())
    mock_get_game.assert_called_once_with("Some Game")
    mock_remove_game.assert_called_once_with(1, 2)

@patch("routes.blacklist_r.log_user_in", return_value={"id": 1})
@patch("routes.blacklist_r.get_blacklist", return_value=[{"title": "Game 1"}, {"title": "Game 2"}])
def test_getblacklist_success(mock_get_blacklist, mock_log_user, client):
    # Test retrieving the blacklist
    response = client.post("/getblacklist", json={"username": "testuser", "password": "testpass"})
    assert response.json == ["Game 1", "Game 2"]
    assert response.status_code == 200
    mock_log_user.assert_called_once_with("testuser", "testpass", client.session_transaction())
    mock_get_blacklist.assert_called_once_with(1)

def test_getblacklist_user_not_logged_in(client):
    # Test calling getblacklist with user not logged in
    response = client.post("/getblacklist", json={})
    assert response.json == {'error': 'User not logged in'}
    assert response.status_code == 401
    