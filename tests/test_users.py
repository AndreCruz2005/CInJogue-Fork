def test_login(client):
    response = client.post("/login", json={"username": "John Doe", "password": "JohnDoePass"})
    assert response.status_code == 200
    assert response.json['username'] == "John Doe"
    assert response.json['email'] == "e@gmail.com" 
    assert 'id' in response.json
    assert 'birthdate' in response.json

def test_login_invalid(client):
    response = client.post("/login", json={"username": "John Doe", "password": "wrongpassword"})
    assert response.status_code == 401
    assert response.json['error'] == "Failed to Login"
    
def test_change_password(client):
    response = client.post("/changepassword", json={"username": "John Doe", "oldPassword": "JohnDoePass", "newPassword": "NewPass"})
    assert response.status_code == 200
    newPassWorks = client.post("/login", json={"username": "John Doe", "password": "NewPass"})
    assert newPassWorks.status_code == 200
    assert newPassWorks.json['username'] == "John Doe"
    
def test_remove_user(client):
    response = client.post("/removeuser", json={"username": "John Doe", "password": "JohnDoePass"})
    assert response.status_code == 200
    assert response.json == True
    
    johnDoeLogin = client.post("/login", json={"username": "John Doe", "password": "JohnDoePass"})
    assert johnDoeLogin.status_code == 401
    assert johnDoeLogin.json['error'] == "Failed to Login"