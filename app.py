from flask import Flask, request, jsonify, session
from flask_cors import CORS
import requests
import random

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "https://freezyyb.github.io"}}, supports_credentials=True)
app.secret_key = "Snowdrop"
from flask import session
app.config["SESSION_COOKIE_HTTPONLY"] = False
app.config["SESSION_COOKIE_SAMESITE"] = "None"
app.config["SESSION_COOKIE_SECURE"] = True

# Enable sessions
app.config["SESSION_TYPE"] = "filesystem"
app.config["SESSION_PERMANENT"] = False

GITHUB_RAW_URL = "https://raw.githubusercontent.com/FreezyyB/Mikasite/main/lines.txt"

# Preset login credentials
USERNAME = "Mika"
PASSWORD = "Puppy#"

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    if data["username"] == USERNAME and data["password"] == PASSWORD:
        session["logged_in"] = True
        return jsonify({"success": True})
    return jsonify({"success": False, "message": "Invalid credentials"}), 401

@app.route('/random-line', methods=['GET'])
def get_random_line():
    if not session.get("logged_in"):
        return jsonify({"error": "Unauthorized"}), 401

    response = requests.get(GITHUB_RAW_URL)

    if response.status_code != 200:
        return jsonify({"error": "Could not fetch data"}), 500
    
    lines = response.text.strip().split("\n")
    if not lines:
        return jsonify({"error": "No lines found"}), 500
    
    random_index = random.randint(0, len(lines) - 1)
    return jsonify({"line": lines[random_index]})

@app.route('/logout', methods=['POST'])
def logout():
    session.pop("logged_in", None)
    return jsonify({"success": True})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
