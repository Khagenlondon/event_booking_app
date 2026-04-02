import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

import pytest
from app_package import create_app
from models import db, User

@pytest.fixture
def app():
    # Creating a test app with in-memory DB
    app = create_app()
    app.config.update(
        TESTING=True,
        SQLALCHEMY_DATABASE_URI="sqlite:///:memory:",
    )
    with app.app_context():
        db.create_all()
    yield app

@pytest.fixture
def client(app):
    return app.test_client()

def test_home_redirects_to_events(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Events" in response.data

def test_register_and_login(client, app):
    # Register
    response = client.post("/register", data={
        "email": "test@example.com",
        "name": "Test User",
        "password": "pass"
    }, follow_redirects=True)
    assert b"Login" in response.data
    # Login
    response = client.post("/login", data={
        "email": "test@example.com",
        "password": "pass"
    }, follow_redirects=True)
    assert b"Logged in successfully" in response.data
