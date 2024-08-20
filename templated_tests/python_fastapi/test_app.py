import pytest
from fastapi.testclient import TestClient
from app import app
from datetime import date

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the FastAPI application!"}

def test_current_date():
    response = client.get("/current-date")
    assert response.status_code == 200
    assert "date" in response.json()

def test_add():
    response = client.get("/add/2/3")
    assert response.status_code == 200
    assert response.json()["result"] == 5

def test_subtract():
    response = client.get("/subtract/5/2")
    assert response.status_code == 200
    assert response.json()["result"] == 3

def test_multiply():
    response = client.get("/multiply/4/5")
    assert response.status_code == 200
    assert response.json()["result"] == 20

def test_divide():
    response = client.get("/divide/10/2")
    assert response.status_code == 200
    assert response.json()["result"] == 5

def test_square():
    response = client.get("/square/4")
    assert response.status_code == 200
    assert response.json()["result"] == 16

def test_age_calculator_invalid_date_format():
    response = client.get("/age-calculator/01-01-2000")
    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid date format. Use YYYY-MM-DD."}


def test_age_calculator_valid_birthdate():
    response = client.get("/age-calculator/2000-01-01")
    assert response.status_code == 200
    assert "birthdate" in response.json()
    assert "age" in response.json()


def test_sum_of_list():
    response = client.get("/sum-of-list/?numbers=1&numbers=2&numbers=3")
    assert response.status_code == 200
    assert response.json() == {"numbers": [1, 2, 3], "sum": 6}


def test_get_weekday_no_date():
    response = client.get("/weekday")
    assert response.status_code == 200
    assert "date" in response.json()
    assert "weekday" in response.json()


def test_leap_year_true():
    response = client.get("/leap-year/2020")
    assert response.status_code == 200
    assert response.json() == {"year": 2020, "is_leap_year": True}


def test_fibonacci_valid_number():
    response = client.get("/fibonacci/5")
    assert response.status_code == 200
    assert response.json() == {"fibonacci": [0, 1, 1, 2, 3]}


def test_factorial_positive_number():
    response = client.get("/factorial/5")
    assert response.status_code == 200
    assert response.json() == {"number": 5, "factorial": 120}


def test_get_weekday_invalid_date_format():
    response = client.get("/weekday?date_str=2021-13-01")
    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid date format. Use YYYY-MM-DD."}


def test_prime_factors_invalid_number():
    response = client.get("/prime-factors/1")
    assert response.status_code == 400
    assert response.json() == {"detail": "Number must be greater than 1"}


def test_fibonacci_invalid_n():
    response = client.get("/fibonacci/0")
    assert response.status_code == 400
    assert response.json() == {"detail": "The number must be greater than 0"}


def test_factorial_negative_number():
    response = client.get("/factorial/-5")
    assert response.status_code == 400
    assert response.json() == {"detail": "Factorial is not defined for negative numbers"}


def test_days_until_new_year():
    response = client.get("/days-until-new-year")
    assert response.status_code == 200
    assert "days_until_new_year" in response.json()


def test_is_palindrome_true():
    response = client.get("/is-palindrome/racecar")
    assert response.status_code == 200
    assert response.json() == {"is_palindrome": True}


def test_divide_by_zero():
    response = client.get("/divide/10/0")
    assert response.status_code == 400
    assert response.json() == {"detail": "Cannot divide by zero"}
