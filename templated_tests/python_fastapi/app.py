
import unittest
from fastapi.testclient import TestClient
from main import app, Item, User

client = TestClient(app)

class TestFastAPI(unittest.TestCase):
    
    def test_root(self):
        response = client.get("/")
        assert response.status_code == 200
        assert response.json() == {"message": "Welcome to the FastAPI application!"}

    def test_random_number_valid(self):
        response = client.get("/random-number?min=0&max=10")
        assert response.status_code == 200
        assert 0 <= response.json()["random_number"] <= 10

    def test_random_number_min_greater_than_max(self):
        response = client.get("/random-number?min=10&max=5")
        assert response.status_code == 400

    def test_create_item(self):
        item_data = {"name": "item1", "price": 10.0}
        response = client.post("/items/", json=item_data)
        assert response.status_code == 200
        assert response.json() == {"item": item_data}

    def test_update_item(self):
        item_data = {"name": "item1", "price": 20.0}
        response = client.put("/items/1", json=item_data)
        assert response.status_code == 200
        assert response.json() == {"item_id": 1, "item": item_data}

    def test_delete_item(self):
        response = client.delete("/items/1")
        assert response.status_code == 200
        assert response.json() == {"message": "Item with id 1 has been deleted"}

    def test_read_users(self):
        response = client.get("/users/?skip=0&limit=2")
        assert response.status_code == 200
        assert len(response.json()) == 2

    def test_create_user(self):
        user_data = {"username": "user1", "email": "user1@example.com", "password": "password"}
        response = client.post("/users/", json=user_data)
        assert response.status_code == 200
        assert response.json() == {"user": user_data}

    def test_update_user(self):
        user_data = {"username": "user1", "email": "user1@example.com", "password": "newpassword"}
        response = client.put("/users/user1", json=user_data)
        assert response.status_code == 200
        assert response.json() == {"username": "user1", "user": user_data}

    def test_date_difference(self):
        response = client.get("/date-difference/?date1=2023-01-01&date2=2023-01-10")
        assert response.status_code == 200
        assert response.json() == {"date_difference": 9}

    def test_factorial(self):
        response = client.get("/factorial/5")
        assert response.status_code == 200
        assert response.json() == {"factorial": 120}

    def test_factorial_negative(self):
        response = client.get("/factorial/-1")
        assert response.status_code == 400

    def test_prime_factors(self):
        response = client.get("/prime-factors/28")
        assert response.status_code == 200
        assert response.json() == {"prime_factors": [2, 2, 7]}

    def test_prime_factors_invalid(self):
        response = client.get("/prime-factors/0")
        assert response.status_code == 400

if __name__ == "__main__":
    unittest.main()
