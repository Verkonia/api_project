from fastapi.testclient import TestClient
import faker
from app.main import app

client = TestClient(app)
fake = faker.Faker()

username = fake.user_name()
password = fake.password()


def test_register():
    response = client.post("/register", params={"username": username, "password": password})
    assert response.status_code == 200


def test_login():
    response = client.post("/register", params={"username": username, "password": password})
    assert response.status_code == 200
    assert "access_token" in response.json()
    global token
    token = response.json()["access_token"]

def test_me():
    response = client.get("/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["username"] == username
