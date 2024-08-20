import io
from openai import OpenAI

client = OpenAI()

template = f"""
import pytest
from fastapi.testclient import TestClient
from app import app
from datetime import date

import math
client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == "message": "Welcome to the FastAPI application!"
"""

# Initialize a buffer to capture the streamed output
output_buffer = io.StringIO()

with open('../templated_tests/python_fastapi/app.py', 'r') as file:
    code = file.read()

# Set up the streaming call
completion = client.chat.completions.create(
    model="gpt-3.5-turbo-0125",
    messages=[
        {"role": "system", "content": "Junior developer with only a few months of experience"},
        {
            "role": "user",
            "content": f"""I've written a Python script, and I'd like you to help me create a suite of unit tests. The test file will be located in the same folder as app.py so import the module as well. Only generate about 7 tests.
             Make use of this template to create the test suite:
             '''
                {template}
             '''
             Here's the code:\n\n{code}\n\nPlease only provide provide the code so that it can run as is. Do not add any additional information or comments. Just the pure code."""
        }
    ],
    stream=True  # Enable streaming
)

for chunk in completion:
    if chunk.choices[0].delta.content is not None:
        content = chunk.choices[0].delta.content.replace("`", "")
        print(chunk.choices[0].delta.content, end="")
        output_buffer.write(chunk.choices[0].delta.content)

# After receiving the entire response, write it to a file
with open('../templated_tests/python_fastapi/test_app.py', 'w') as file:
    file.write(output_buffer.getvalue().replace("`", "").replace("python", ""))