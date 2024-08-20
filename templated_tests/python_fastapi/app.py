from fastapi import FastAPI, HTTPException, Query
from datetime import date, datetime, timedelta
from typing import List, Optional

app = FastAPI()

@app.get("/")
async def root():
    """
    A simple function that serves as the root endpoint for the FastAPI application.
    Returns a dictionary with a welcome message.
    """
    return {"message": "Welcome to the FastAPI application!"}

@app.get("/current-date")
async def current_date():
    """
    Get the current date as an ISO-formatted string.
    """
    return {"date": date.today().isoformat()}

@app.get("/add/{num1}/{num2}")
async def add(num1: int, num2: int):
    """
    Adds two numbers and returns the result.
    """
    return {"result": num1 + num2}

@app.get("/subtract/{num1}/{num2}")
async def subtract(num1: int, num2: int):
    """
    Subtracts the second number from the first and returns the result.
    """
    return {"result": num1 - num2}

@app.get("/multiply/{num1}/{num2}")
async def multiply(num1: int, num2: int):
    """
    Multiplies two numbers and returns the result.
    """
    return {"result": num1 * num2}

@app.get("/divide/{num1}/{num2}")
async def divide(num1: int, num2: int):
    """
    Divides the first number by the second and returns the result.
    Raises an exception if division by zero is attempted.
    """
    if num2 == 0:
        raise HTTPException(status_code=400, detail="Cannot divide by zero")
    return {"result": num1 / num2}

@app.get("/square/{number}")
async def square(number: int):
    """
    Returns the square of a number.
    """
    return {"result": number**2}

@app.get("/is-palindrome/{text}")
async def is_palindrome(text: str):
    """
    Checks if the provided string is a palindrome.
    """
    return {"is_palindrome": text == text[::-1]}

@app.get("/days-until-new-year")
async def days_until_new_year():
    """
    Calculates the number of days until the next New Year.
    """
    today = date.today()
    next_new_year = date(today.year + 1, 1, 1)
    delta = next_new_year - today
    return {"days_until_new_year": delta.days}

@app.get("/echo/{message}")
async def echo(message: str):
    """
    Returns the same message that is sent to it.
    """
    return {"message": message}

@app.post("/reverse-words/")
async def reverse_words(sentence: str):
    """
    Reverses the order of words in the provided sentence.
    """
    words = sentence.split()
    reversed_sentence = " ".join(reversed(words))
    return {"original": sentence, "reversed": reversed_sentence}

@app.get("/factorial/{number}")
async def factorial(number: int):
    """
    Computes the factorial of a number.
    """
    if number < 0:
        raise HTTPException(status_code=400, detail="Factorial is not defined for negative numbers")
    fact = 1
    for i in range(2, number + 1):
        fact *= i
    return {"number": number, "factorial": fact}

@app.get("/fibonacci/{n}")
async def fibonacci(n: int):
    """
    Generates the first 'n' numbers of the Fibonacci sequence.
    """
    if n < 1:
        raise HTTPException(status_code=400, detail="The number must be greater than 0")
    fib_sequence = [0, 1]
    for i in range(2, n):
        fib_sequence.append(fib_sequence[-1] + fib_sequence[-2])
    return {"fibonacci": fib_sequence[:n]}

@app.get("/leap-year/{year}")
async def leap_year(year: int):
    """
    Determines if a given year is a leap year.
    """
    is_leap = (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)
    return {"year": year, "is_leap_year": is_leap}

@app.get("/prime-factors/{number}")
async def prime_factors(number: int):
    """
    Returns the prime factors of a given number.
    """
    if number <= 1:
        raise HTTPException(status_code=400, detail="Number must be greater than 1")
    
    i = 2
    factors = []
    while i * i <= number:
        if number % i:
            i += 1
        else:
            number //= i
            factors.append(i)
    if number > 1:
        factors.append(number)
    
    return {"number": number, "prime_factors": factors}

@app.get("/weekday")
async def get_weekday(date_str: Optional[str] = None):
    """
    Returns the day of the week for a given date. If no date is provided, returns the current weekday.
    """
    if date_str:
        try:
            date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD.")
    else:
        date_obj = date.today()

    return {"date": date_obj.isoformat(), "weekday": date_obj.strftime("%A")}

@app.get("/sum-of-list/")
async def sum_of_list(numbers: List[int] = Query(...)):
    """
    Returns the sum of a list of numbers.
    """
    return {"numbers": numbers, "sum": sum(numbers)}

@app.get("/age-calculator/{birthdate}")
async def age_calculator(birthdate: str):
    """
    Calculates the age of a person given their birthdate in YYYY-MM-DD format.
    """
    try:
        birth_date = datetime.strptime(birthdate, "%Y-%m-%d").date()
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD.")
    
    today = date.today()
    age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))

    return {"birthdate": birthdate, "age": age}
