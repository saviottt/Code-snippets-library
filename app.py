from flask import Flask, request
from supabase import create_client

app = Flask(__name__)

SUPABASE_URL = "https://vqotlplzwqrxtmnqovpv.supabase.co"
SUPABASE_KEY = "sb_publishable_nJpoJ4cJrv4ArJs4xa-xmg_tIrhqh3Z"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


@app.route("/")
def home():
    return open("index.html").read()


@app.route("/register", methods=["POST"])
def register():

    name = request.form["name"]
    email = request.form["email"]
    password = request.form["password"]

    data = {
        "name": name,
        "email": email,
        "password": password
    }

    response = supabase.table("students").insert(data).execute()

    return "Student details stored successfully!"


if __name__ == "__main__":
    app.run(debug=True)