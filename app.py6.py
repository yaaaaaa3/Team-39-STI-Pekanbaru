def get_fingerprint():
    try:
        response = requests.get(f"{API_URL}/get_fingerprint")
        response.raise_for_status()  # Raise an error for bad responses
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching fingerprint: {e}")
        return {'finger_id': -1}

def classify_weight(weight):
    try:
        response = requests.post(f"{API_URL}/classify_weight", json={"weight": weight})
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error classifying weight: {e}")
        return {'user': 'Unknown', 'probability': 0.0}

def control_servo(action):
    try:
        response = requests.post(f"{API_URL}/control_servo", json={"action": action})
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error controlling servo: {e}")
        return {'status': 'error', 'message': 'Failed to control servo'}
