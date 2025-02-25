from flask_cors import CORS

from flask import Flask, request, jsonify
import firebase_admin
from firebase_admin import credentials, db

# Initialize Firebase
cred = credentials.Certificate("firebase-key.json")  # Ensure this file is in your project folder
firebase_admin.initialize_app(cred, {
    "databaseURL": "https://attendease-817f6-default-rtdb.asia-southeast1.firebasedatabase.app"
})

app = Flask(__name__)
CORS(app)

# Default route to check if the API is working
@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Welcome to AttendEase API!"})


# ✅ Register User API
@app.route("/register", methods=["POST"])
def register_user():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    users_ref = db.reference("users")
    if users_ref.child(username).get():
        return jsonify({"message": "User already exists!"}), 400

    users_ref.child(username).set({"password": password})
    return jsonify({"message": f"User '{username}' registered successfully!"}), 201

# ✅ Login API
@app.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    users_ref = db.reference("users/" + username)
    user = users_ref.get()

    if not user:
        return jsonify({"message": "User not found!"}), 401

    if str(user["password"]) != str(password):
        return jsonify({"message": "Invalid password!"}), 401

    return jsonify({"message": "Login successful!"}), 200

# Start Flask Server
if __name__ == "__main__":
    app.run(debug=True, port=5000)  # Change port if needed
