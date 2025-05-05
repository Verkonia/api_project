from fastapi.testclient import TestClient
import faker
from app.main import app

client = TestClient(app)
fake = faker.Faker()

username = fake.user_name()
password = fake.password()

movie_data = {
    'title': 'visit',
    'description': 'desc',
    'year': 2013, 
    'genre': 'horror',  
    'director': 'sh',
    'rating': 10
}


def test_register():
    response = client.post('/register', params={'username': username, 'password': password})
    assert response.status_code == 200


def get_token():
    response = client.post(
        '/token',
        data={
            'username': username,
            'password': password,
            'grant_type': 'password',
            'scope': '',
            'client_id': '',
            'client_secret': ''
        },
        headers={'Content-Type': 'application/x-www-form-urlencoded'}
    )
    assert response.status_code == 200
    assert 'access_token' in response.json()
    return response.json()['access_token']

def test_protected_endpoint():
    token = get_token() 
    response = client.get(
        '/me', 
        headers={'Authorization': f'Bearer {token}'}
    )
    assert response.status_code == 200
    assert 'username' in response.json()

def test_invalid_credentials():
    response = client.post(
        '/token',
        data={
            'username': 'wronguser',
            'password': 'wrongpass',
            'grant_type': 'password'
        },
        headers={'Content-Type': 'application/x-www-form-urlencoded'}
    )
    assert response.status_code == 400
    
def test_create_movie():
    token = get_token()
    response = client.post(
        '/movies/',
        json=movie_data,
        headers={
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
    )
    assert response.status_code == 200
    
def test_create_rating():
    token = get_token()
    response = client.post(
        '/ratings/',
        json=movie_data,
        headers={
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
    )
    assert response.status_code == 200

def test_search_movie_by_title():

    test_title = 'visit' 
    response = client.get(
        '/movies/get/',
        params={'title': test_title},  
        headers={'Accept': 'application/json'}
    )
    
    assert response.status_code == 200
