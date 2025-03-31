import pytest

def test_promptAI_recommend(client):
    # Log in and send a prompt
    response = client.post('/genai', json={"username": "John Doe", "password": "JohnDoePass", "prompt": "Recommend games"})
    assert response.status_code == 200

    # Check if the recommendations were updated
    recommendations = response.get_json()
    assert isinstance(recommendations, list)
    assert recommendations[0]['command'] == "Recommend"
    assert isinstance(recommendations[0]['titles'], list)
    assert len(recommendations[0]['titles']) > 0

def test_promptAI_add(client):
    # Log in and send a prompt
    response = client.post('/genai', json={"username": "John Doe", "password": "JohnDoePass", "prompt": "Add game1 to my library"})
    assert response.status_code == 200

    # Check if the response matches the mock
    response_data = response.get_json()
    assert isinstance(response_data, list)
    assert response_data[0]['command'] == "Add"
    assert response_data[0]['titles'] == ["game1"]

def test_promptAI_remove(client):
    # Log in and send a prompt
    response = client.post('/genai', json={"username": "John Doe", "password": "JohnDoePass", "prompt": "Remove game1 from my library"})
    assert response.status_code == 200

    # Check if the response matches the mock
    response_data = response.get_json()
    assert isinstance(response_data, list)
    assert response_data[0]['command'] == "Remove"
    assert response_data[0]['titles'] == ["game1"]

def test_promptAI_rate(client):
    # Log in and send a prompt
    response = client.post('/genai', json={"username": "John Doe", "password": "JohnDoePass", "prompt": "Rate game1 with 5 stars"})
    assert response.status_code == 200

    # Check if the response matches the mock
    response_data = response.get_json()
    assert isinstance(response_data, list)
    assert response_data[0]['command'] == "Rate"
    assert response_data[0]['titles'] == ["game1"]
    assert response_data[0]['other'] == [5]

def test_promptAI_state(client):
    # Log in and send a prompt
    response = client.post('/genai', json={"username": "John Doe", "password": "JohnDoePass", "prompt": "Mark game1 as completed"})
    assert response.status_code == 200

    # Check if the response matches the mock
    response_data = response.get_json()
    assert isinstance(response_data, list)
    assert response_data[0]['command'] == "State"
    assert response_data[0]['titles'] == ["game1"]
    assert response_data[0]['other'] == ["CONCLUÍDO"]

def test_promptAI_unauthorized(client):
    # Attempt to send a prompt without valid credentials
    response = client.post('/genai', json={"username": "InvalidUser", "password": "InvalidPass", "prompt": "Recommend games"})
    assert response.status_code == 401
    assert response.get_json() == {'error': 'User not logged in'}