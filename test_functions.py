import requests
import logging

logging.basicConfig(level=logging.INFO)

def register_user(username, password, base_url="http://127.0.0.1:8000"):
    try:
        response = requests.post(
            f"{base_url}/register",
            json={"username": username, "password": password}
        )
        response.raise_for_status()
        return response
    except requests.exceptions.RequestException as e:
        logging.error(f"Registration failed for user {username}: {e}")
        raise

def get_polls(skip=0, limit=10, base_url="http://127.0.0.1:8000"):
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
    try:
        response = requests.post(
            f"{base_url}/polls",
            json={"question": question, "options": options},
            headers={"Authorization": f"Bearer {access_token}"}
        )
        response.raise_for_status()
        return response
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to create poll '{question}': {e}")
        raise

def vote_on_poll(poll_id, option_id, access_token, base_url="http://127.0.0.1:8000"):
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
    try:
        response = requests.get(f"{base_url}/polls/{poll_id}/results")
        response.raise_for_status()
        return response
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to get results for poll {poll_id}: {e}")
        raise

# Test the functions
if __name__ == "__main__":
    # Register
    resp = register_user("testuser", "testpass")
    print(f"Register: {resp.status_code}, User: {resp.json()}")
    
    # Login to get token
    login_resp = requests.post("http://127.0.0.1:8000/login", data={"username": "testuser", "password": "testpass"})
    token = login_resp.json()["access_token"]
    
    # Get polls
    resp = get_polls()
    print(f"Get polls: {resp.status_code}, Count: {len(resp.json())}")
    
    # Create poll
    resp = create_poll("Test question?", ["Option A", "Option B"], token)
    poll_data = resp.json()
    print(f"Create poll: {resp.status_code}, Poll ID: {poll_data['id']}")
    
    # Vote
    resp = vote_on_poll(poll_data['id'], poll_data['options'][0]['id'], token)
    print(f"Vote: {resp.status_code}, Vote ID: {resp.json()['id']}")
    
    # Get results
    resp = get_poll_results(poll_data['id'])
    print(f"Results: {resp.status_code}, Results: {resp.json()}")
    
    # Delete poll
    resp = delete_poll(poll_data['id'], token)
    print(f"Delete poll: {resp.status_code}")