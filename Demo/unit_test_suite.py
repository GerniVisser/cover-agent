
import unittest
from fastapi.testclient import TestClient
from your_module import app  # Replace 'your_module' with the actual name of your module

client = TestClient(app)

class TestFastAPI(unittest.TestCase):

    def test_root(self):
        response = client.get("/")
        assert response.status_code == 200
        assert response.json() == {"message": "Welcome to the FastAPI application!"}

    def test_random_number(self):
        response = client.get("/random-number?min=1&max=10")
        assert response.status_code == 200
        assert 1 <= response.json()["random_number"] <= 10

    def test_random_number_invalid(self):
        response = client.get("/random-number?min=10&max=1")
        assert response.status_code == 400
        assert response.json() == {"detail": "Min cannot be greater than Max"}

    def test_create_item(self):
        response = client.post("/items/", json={"name": "Test Item", "price": 10.0})
        assert response.status_code == 200
        assert response.json() == {"item": {"name": "Test Item", "description": None, "price": 10.0, "tax": None}}

    def test_update_item(self):
        response = client.put("/items/1", json={"name": "Updated Item", "price": 15.0})
        assert response.status_code == 200
        assert response.json() == {"item_id": 1, "item": {"name": "Updated Item", "description": None, "price": 15.0, "tax": None}}

    def test_delete_item(self):
        response = client.delete("/items/1")
        assert response.status_code == 200
        assert response.json() == {"message": "Item with id 1 has been deleted"}

    def test_read_users(self):
        response = client.get("/users/?skip=0&limit=2")
        assert response.status_code == 200
        assert len(response.json()) == 2

    def test_create_user(self):
        response = client.post("/users/", json={"username": "testuser", "email": "test@example.com", "password": "password"})
        assert response.status_code == 200
        assert response.json() == {"user": {"username": "testuser", "email": "test@example.com", "full_name": None, "password": "password"}}

    def test_update_user(self):
        response = client.put("/users/testuser", json={"username": "updateduser", "email": "updated@example.com", "password": "newpassword"})
        assert response.status_code == 200
        assert response.json() == {"username": "updateduser", "user": {"username": "updateduser", "email": "updated@example.com", "full_name": None, "password": "newpassword"}}

    def test_date_difference(self):
        response = client.get("/date-difference/?date1=2023-10-01&date2=2023-10-10")
        assert response.status_code == 200
        assert response.json() == {"date_difference": 9}

    def test_factorial(self):
        response = client.get("/factorial/5")
        assert response.status_code == 200
        assert response.json() == {"factorial": 120}

    def test_factorial_negative(self):
        response = client.get("/factorial/-5")
        assert response.status_code == 400
        assert response.json() == {"detail": "Cannot calculate factorial of a negative number"}

    def test_prime_factors(self):
        response = client.get("/prime-factors/28")
        assert response.status_code == 200
        assert response.json() == {"prime_factors": [2, 2, 7]}

    def test_prime_factors_invalid(self):
        response = client.get("/prime-factors/0")
        assert response.status_code == 400
        assert response.json() == {"detail": "Number must be greater than 0"}

if __name__ == "__main__":
    unittest.main()
