import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base
from main import app
from auth import get_db, get_password_hash
from models import User

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

@pytest.fixture(scope="module", autouse=True)
def setup_database():
    # Drop all tables and recreate them
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    
    db = TestingSessionLocal()
    hashed_password = get_password_hash("password")
    db_user = User(username="admin", hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.close()

def test_create_employee():
    # First, get token
    response = client.post("/token", data={"username": "admin", "password": "password"})
    assert response.status_code == 200
    token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    employee_data = {
        "name": "John Doe",
        "email": "john@example.com",
        "department": "Engineering",
        "role": "Developer"
    }
    response = client.post("/api/employees/", json=employee_data, headers=headers)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "John Doe"
    assert data["email"] == "john@example.com"

def test_create_employee_duplicate_email():
    response = client.post("/token", data={"username": "admin", "password": "password"})
    token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    employee_data = {
        "name": "Jane Doe",
        "email": "john@example.com",  # duplicate
        "department": "HR",
        "role": "Manager"
    }
    response = client.post("/api/employees/", json=employee_data, headers=headers)
    assert response.status_code == 400

def test_list_employees():
    response = client.post("/token", data={"username": "admin", "password": "password"})
    token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    response = client.get("/api/employees/", headers=headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_employee():
    response = client.post("/token", data={"username": "admin", "password": "password"})
    token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    response = client.get("/api/employees/1", headers=headers)
    if response.status_code == 200:
        data = response.json()
        assert data["id"] == 1
    else:
        assert response.status_code == 404

def test_update_employee():
    response = client.post("/token", data={"username": "admin", "password": "password"})
    token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    update_data = {"name": "John Smith"}
    response = client.put("/api/employees/1", json=update_data, headers=headers)
    if response.status_code == 200:
        data = response.json()
        assert data["name"] == "John Smith"
    else:
        assert response.status_code == 404

def test_delete_employee():
    response = client.post("/token", data={"username": "admin", "password": "password"})
    token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    response = client.delete("/api/employees/1", headers=headers)
    if response.status_code == 204:
        # Check if deleted
        response = client.get("/api/employees/1", headers=headers)
        assert response.status_code == 404
    else:
        assert response.status_code == 404