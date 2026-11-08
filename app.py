from flask import Flask, render_template, request, jsonify, session
from supabase import create_client
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "change-this-secret")

supabase = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_KEY")
)


@app.route("/")
def home():
    return render_template("index.html")


# REGISTER
@app.route("/register", methods=["POST"])
def register():

    data = request.json

    name = data.get("name")
    email = data.get("email")
    password = data.get("password")

    try:
        response = supabase.auth.sign_up({
            "email": email,
            "password": password,
            "options": {
                "data": {
                    "name": name
                }
            }
        })

        return jsonify({
            "success": True,
            "message": "Registration successful! Check your email if confirmation is enabled."
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        }), 400


# LOGIN
@app.route("/login", methods=["POST"])
def login():

    data = request.json

    email = data.get("email")
    password = data.get("password")

    try:
        response = supabase.auth.sign_in_with_password({
            "email": email,
            "password": password
        })

        session["access_token"] = response.session.access_token
        session["refresh_token"] = response.session.refresh_token
        session["user"] = {
            "email": response.user.email,
            "name": response.user.user_metadata.get("name", "")
        }

        return jsonify({
            "success": True,
            "message": "Login successful!",
            "user": session["user"]
        })

    except Exception:
        return jsonify({
            "success": False,
            "message": "Invalid email or password."
        }), 401


# DASHBOARD
@app.route("/dashboard")
def dashboard():

    if "user" not in session:
        return jsonify({"message": "Please login first"}), 401

    return jsonify({
        "message": "Welcome!",
        "user": session["user"]
    })


# LOGOUT
@app.route("/logout", methods=["POST"])
def logout():

    session.clear()

    return jsonify({
        "success": True,
        "message": "Logged out successfully"
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5000)
