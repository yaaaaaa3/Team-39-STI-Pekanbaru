import streamlit as st
import requests
from flask import Flask, request, jsonify
import threading
import random
import time

# Initialize Flask API
app = Flask(__name__)

# Mock function for fingerprint ID (simulate with random data)
def get_fingerprint_id():
    # In real implementation, you would read from the sensor
    return random.choice([1, 2, -1])  # Simulating User A, User B, or no match

# Mock function to classify weight (simulate with random data)
def classify_weight(weight):
    if weight < 49.0:
        return "User A", random.uniform(0.4, 0.6)
    else:
        return "User B", random.uniform(0.6, 0.8)

@app.route('/get_fingerprint', methods=['GET'])
def get_fingerprint():
    finger_id = get_fingerprint_id()
    return jsonify({'finger_id': finger_id})

@app.route('/classify_weight', methods=['POST'])
def classify_weight_route():
    weight = request.json['weight']
    user, prob = classify_weight(weight)
    return jsonify({'user': user, 'probability': prob})

@app.route('/control_servo', methods=['POST'])
def control_servo():
    action = request.json['action']  # 'open' or 'close'
    if action == 'open':
        # Send command to ESP32 to open the door (e.g., set servo angle to 160)
        print("Servo opened")
        return jsonify({'status': 'success', 'message': 'Door opened'})
    elif action == 'close':
        # Send command to ESP32 to close the door (e.g., set servo angle to 15)
        print("Servo closed")
        return jsonify({'status': 'success', 'message': 'Door closed'})
    else:
        return jsonify({'status': 'error', 'message': 'Invalid action'})

# Run the Flask app in a separate thread
def run_flask():
    app.run(debug=False, host='0.0.0.0', port=5000)

# Start Flask server in a new thread
flask_thread = threading.Thread(target=run_flask)
flask_thread.daemon = True
flask_thread.start()

# Streamlit frontend
def streamlit_app():
    # Define API URL (for communication with Flask API)
    API_URL = "http://127.0.0.1:5000"  # Adjust the URL if needed

    def get_fingerprint():
        response = requests.get(f"{API_URL}/get_fingerprint")
        return response.json()

    def classify_weight(weight):
        response = requests.post(f"{API_URL}/classify_weight", json={"weight": weight})
        return response.json()

    def control_servo(action):
        response = requests.post(f"{API_URL}/control_servo", json={"action": action})
        return response.json()

    # Streamlit frontend
    st.title("Smart Security System")
    st.write("Welcome to the Smart Security System powered by ESP32")

    # Input for weight
    weight = st.number_input("Enter weight (kg)", min_value=40.0, max_value=100.0, step=0.1)

    # Classify weight
    if st.button("Classify User"):
        st.write("Classifying weight...")
        result = classify_weight(weight)
        st.write(f"User: {result['user']}")
        st.write(f"Probability: {result['probability']:.2f}")

    # Fingerprint check
    if st.button("Check Fingerprint"):
        st.write("Checking fingerprint...")
        result = get_fingerprint()
        if result['finger_id'] == 1:
            st.write("Fingerprint matched with User A!")
        elif result['finger_id'] == 2:
            st.write("Fingerprint matched with User B!")
        else:
            st.write("No fingerprint match found.")

    # Control servo
    action = st.selectbox("Control Door", ["open", "close"])

    if st.button(f"{action.capitalize()} Door"):
        result = control_servo(action)
        st.write(result['message'])

    # Add some visuals or further details here based on sensor data
    st.write("System Status: Running")

# Run Streamlit app
if __name__ == "__main__":
    streamlit_app()

