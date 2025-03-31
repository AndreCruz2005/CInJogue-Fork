def test_tags(client):
    addition = client.post("/addtags", json={"text": "tag1", "tag_type": "type1", "username": "John Doe", "password": "JohnDoePass"})
    assert addition.status_code == 201
    assert addition.json == True
    
    get = client.post("/gettags", json={"username": "John Doe", "password": "JohnDoePass"})
    assert get.status_code == 200
    assert get.json == {'type1': ['tag1']}
    
    remove = client.post("/removetags", json={"text": "tag1", "username": "John Doe", "password": "JohnDoePass"})
    assert remove.status_code == 200
    assert remove.json == True
    
    get = client.post("/gettags", json={"username": "John Doe", "password": "JohnDoePass"})
    assert get.status_code == 200
    assert get.json == {}
    
def test_tags_user_not_logged_in(client):
    addition = client.post("/addtags", json={"text": "tag1", "tag_type": "type1", "username": "John Not Doe", "password": "JohnDoePass"})
    assert addition.status_code == 401
    assert addition.json == {'error':'User not logged in'}
    
    get = client.post("/gettags", json={"username": "John Not Doe", "password": "JohnDoePass"})
    assert get.status_code == 401
    assert get.json == {'error':'User not logged in'}
    
    remove = client.post("/removetags", json={"text": "tag1", "username": "John Not Doe", "password": "JohnDoePass"})
    assert remove.status_code == 401
    assert remove.json == {'error':'User not logged in'}
    
    get = client.post("/gettags", json={"username": "John Not Doe", "password": "JohnDoePass"})
    assert get.status_code == 401
    assert get.json == {'error':'User not logged in'}
    
    
    
