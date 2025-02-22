from flask import Flask, request, jsonify, session
import requests

app = Flask(__name__)
app.secret_key = "Snowdrop"

# Enable sessions
app.config["SESSION_TYPE"] = "filesystem"
app.config["SESSION_PERMANENT"] = False

GOOGLE_SCRIPT_URL = "1kQcyzPScpeIJgwMm9cbP10G0oiZLPUmVixnZSUP_z7n5vPmkZ2SFE8MA"

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

    response = requests.get(GOOGLE_SCRIPT_URL)
    return jsonify({"line": response.text})

@app.route('/logout', methods=['POST'])
def logout():
    session.pop("logged_in", None)
    return jsonify({"success": True})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
