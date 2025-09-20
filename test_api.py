import requests

BASE_URL = "http://127.0.0.1:8000"

# Register user
response = requests.post(f"{BASE_URL}/register", json={"username": "test", "password": "test123"})
print(f"Register: {response.status_code}")

# Login
response = requests.post(f"{BASE_URL}/login", data={"username": "test", "password": "test123"})
token = response.json()["access_token"]
print(f"Login: {response.status_code}")

# Create poll
response = requests.post(
    f"{BASE_URL}/polls",
    json={"question": "Test poll?", "options": ["Yes", "No"]},
    headers={"Authorization": f"Bearer {token}"}
)
poll_id = response.json()["id"]
print(f"Create poll: {response.status_code}")

# Vote
response = requests.post(
    f"{BASE_URL}/polls/{poll_id}/vote",
    json={"option_id": 1},
    headers={"Authorization": f"Bearer {token}"}
)
print(f"Vote: {response.status_code}")

# Get results
response = requests.get(f"{BASE_URL}/polls/{poll_id}/results")
print(f"Results: {response.status_code}")
print("All tests completed!")