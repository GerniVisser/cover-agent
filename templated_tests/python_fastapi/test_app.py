import pytest
from fastapi.testclient import TestClient
from app import app
from datetime import date

client = TestClient(app)

def test_root():
    """
    Test the root endpoint by sending a GET request to "/" and checking the response status code and JSON body.
    """
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the FastAPI application!"}

def test_prime_factors_invalid():
    response = client.get("/prime-factors/0")
    assert response.status_code == 400
    assert response.json() == {"detail": "Number must be greater than 0"}


def test_prime_factors_valid():
    response = client.get("/prime-factors/28")
    assert response.status_code == 200
    assert response.json() == {"prime_factors": [2, 2, 7]}


def test_factorial_invalid():
    response = client.get("/factorial/-5")
    assert response.status_code == 400
    assert response.json() == {"detail": "Cannot calculate factorial of a negative number"}


def test_factorial_valid():
    response = client.get("/factorial/5")
    assert response.status_code == 200
    assert response.json() == {"factorial": 120}


def test_date_difference():
    response = client.get("/date-difference/?date1=2023-01-01&date2=2023-01-10")
    assert response.status_code == 200
    assert response.json() == {"date_difference": 9}


def test_update_user():
    user_data = {"username": "updateduser", "email": "updateduser@example.com", "full_name": "Updated User", "password": "newpassword123"}
    response = client.put("/users/testuser", json=user_data)
    assert response.status_code == 200
    assert response.json() == {"username": "testuser", "user": user_data}


def test_create_user():
    user_data = {"username": "testuser", "email": "testuser@example.com", "full_name": "Test User", "password": "password123"}
    response = client.post("/users/", json=user_data)
    assert response.status_code == 200
    assert response.json() == {"user": user_data}


def test_read_users():
    response = client.get("/users/")
    assert response.status_code == 200
    assert len(response.json()) == 10


def test_delete_item():
    response = client.delete("/items/1")
    assert response.status_code == 200
    assert response.json() == {"message": "Item with id 1 has been deleted"}


def test_update_item():
    item_data = {"name": "Updated Item", "description": "An updated item", "price": 15.0, "tax": 2.0}
    response = client.put("/items/1", json=item_data)
    assert response.status_code == 200
    assert response.json() == {"item_id": 1, "item": item_data}


def test_create_item():
    item_data = {"name": "Test Item", "description": "A test item", "price": 10.5, "tax": 1.5}
    response = client.post("/items/", json=item_data)
    assert response.status_code == 200
    assert response.json() == {"item": item_data}


def test_random_number_invalid():
    response = client.get("/random-number?min=20&max=10")
    assert response.status_code == 400
    assert response.json() == {"detail": "Min cannot be greater than Max"}


def test_random_number_valid():
    response = client.get("/random-number?min=10&max=20")
    assert response.status_code == 200
    assert 10 <= response.json()["random_number"] <= 20
