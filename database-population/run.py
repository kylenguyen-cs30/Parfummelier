import requests
import random
import string
from faker import Faker

# Initialize Faker for generating random data
fake = Faker()

# Define the API endpoint
url = "http://localhost:5001/register"


# Function to generate random strong password
def generate_password(length=12):
    characters = string.ascii_letters + string.digits + string.punctuation
    password = "".join(random.choice(characters) for i in range(length))
    return password


# Generate 10 random users
for _ in range(10):
    first_name = fake.first_name()
    last_name = fake.last_name()
    email = f"{first_name.lower()}.{last_name.lower()}@something.com"
    password = generate_password()
    user_name = f"{first_name.lower()}{last_name.lower()}"
    dob = fake.date_of_birth(minimum_age=18, maximum_age=60).strftime("%Y-%m-%d")

    # Data to be sent to the API
    user_data = {
        "firstName": first_name,
        "lastName": last_name,
        "email": email,
        "password": password,
        "userName": user_name,
        "dob": dob,
    }

    # Send the POST request to the API
    response = requests.post(url, json=user_data)

    # Print response for each user
    if response.status_code == 201:
        print(f"User {user_name} registered successfully.")
    else:
        print(
            f"Failed to register user {user_name}. Response: {response.status_code} - {response.text}"
        )
