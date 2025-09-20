"""Polly API Client Functions

Usage Example:
    # Register and login
    resp = register_user("myuser", "mypass")
    login_resp = requests.post("http://127.0.0.1:8000/login", 
                              data={"username": "myuser", "password": "mypass"})
    token = login_resp.json()["access_token"]
    
    # Create and vote on poll
    poll_resp = create_poll("Favorite color?", ["Red", "Blue"], token)
    poll_id = poll_resp.json()["id"]
    vote_on_poll(poll_id, poll_resp.json()["options"][0]["id"], token)
    
    # Get results
    results = get_poll_results(poll_id)
"""

import requests
import logging

logging.basicConfig(level=logging.INFO)

def register_user(username, password, base_url="http://127.0.0.1:8000"):
    """Register a new user via /register endpoint."""
    try:
        response = requests.post(
            f"{base_url}/register",
            json={"username": username, "password": password}
        )
        response.raise_for_status()
        return response
    except requests.exceptions.RequestException as e:
        logging.error(f"Registration failed: {e}")
        raise

def get_polls(skip=0, limit=10, base_url="http://127.0.0.1:8000"):
    """Fetch paginated polls from /polls endpoint."""
    try:
        response = requests.get(
            f"{base_url}/polls",
            params={"skip": skip, "limit": limit}
        )
        response.raise_for_status()
        return response
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to fetch polls: {e}")
        raise

def create_poll(question, options, access_token, base_url="http://127.0.0.1:8000"):
    """Create a new poll with question and options (requires auth)."""
    if len(options) < 2:
        raise ValueError("At least two options are required")
    try:
        response = requests.post(
            f"{base_url}/polls",
            json={"question": question, "options": options},
            headers={"Authorization": f"Bearer {access_token}"}
        )
        response.raise_for_status()
        return response
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to create poll: {e}")
        raise

def vote_on_poll(poll_id, option_id, access_token, base_url="http://127.0.0.1:8000"):
    """Cast a vote on a poll option (requires auth)."""
    try:
        response = requests.post(
            f"{base_url}/polls/{poll_id}/vote",
            json={"option_id": option_id},
            headers={"Authorization": f"Bearer {access_token}"}
        )
        response.raise_for_status()
        return response
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to vote on poll {poll_id}: {e}")
        raise

def delete_poll(poll_id, access_token, base_url="http://127.0.0.1:8000"):
    """Delete a poll by ID (requires auth)."""
    try:
        response = requests.delete(
            f"{base_url}/polls/{poll_id}",
            headers={"Authorization": f"Bearer {access_token}"}
        )
        response.raise_for_status()
        return response
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to delete poll {poll_id}: {e}")
        raise

def get_poll_results(poll_id, base_url="http://127.0.0.1:8000"):
    """Get poll results with vote counts by poll ID."""
    try:
        response = requests.get(f"{base_url}/polls/{poll_id}/results")
        response.raise_for_status()
        return response
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to get results for poll {poll_id}: {e}")
        raise

# Test the functions
if __name__ == "__main__":
    import random
    test_user = f"testuser{random.randint(1000, 9999)}"
    
    # Register
    resp = register_user(test_user, "testpass")
    user_data = resp.json()
    print(f"Register: {resp.status_code}, User ID: {user_data.get('id')}")
    
    # Login to get token
    try:
        login_resp = requests.post("http://127.0.0.1:8000/login", data={"username": test_user, "password": "testpass"})
        login_resp.raise_for_status()
        token = login_resp.json()["access_token"]
    except requests.exceptions.RequestException as e:
        logging.error(f"Login failed: {e}")
        raise
    except KeyError:
        logging.error("Login response missing access_token")
        raise
    
    # Get polls
    resp = get_polls()
    print(f"Get polls: {resp.status_code}, Count: {len(resp.json())}")
    
    # Create poll
    resp = create_poll("Test question?", ["Option A", "Option B"], token)
    poll_data = resp.json()
    print(f"Create poll: {resp.status_code}, Poll ID: {poll_data['id']}")
    
    # Vote
    resp = vote_on_poll(poll_data['id'], poll_data['options'][0]['id'], token)
    vote_data = resp.json()
    print(f"Vote: {resp.status_code}, Vote ID: {vote_data.get('id')}")
    
    # Get results
    resp = get_poll_results(poll_data['id'])
    results_data = resp.json()
    print(f"Results: {resp.status_code}, Poll: {results_data.get('question')}")
    
    # Delete poll
    resp = delete_poll(poll_data['id'], token)
    print(f"Delete poll: {resp.status_code}")