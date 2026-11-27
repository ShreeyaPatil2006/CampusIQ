import os
os.environ["ADMIN_EMAIL"] = "admin@campusiq.demo"
os.environ["ADMIN_PASSWORD"] = "CampusIQ@123"
os.environ["DATABASE_URL"] = "sqlite://"
os.environ["FLASK_SECRET_KEY"] = "test-secret"

from app import create_app
from app.extensions import db

def setup_function():
    global app, client
    app = create_app()
    app.config["TESTING"] = True
    with app.app_context():
        db.drop_all()
        db.create_all()
        from app.seed import seed_database
        seed_database()
    client = app.test_client()

def test_health():
    assert client.get("/api/health").status_code == 200

def test_chat_retrieves_attendance():
    response = client.post("/api/chat", json={"message": "How many lectures do I need to attend?"})
    assert response.status_code == 200
    assert "75%" in response.get_json()["answer"]

def test_empty_chat_rejected():
    assert client.post("/api/chat", json={"message": ""}).status_code == 400

def test_admin_authentication():
    response = client.post("/api/auth/login", json={"email": "admin@campusiq.demo", "password": "CampusIQ@123"})
    assert response.status_code == 200
