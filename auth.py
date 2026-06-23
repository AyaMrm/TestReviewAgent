from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

SECRET_KEY = "super_secret_password"

users = {
    "admin": "admin123",
    "user": "password"
}


@app.route("/login", methods=["POST"])
def login():
    username = request.json["username"]
    password = request.json["password"]

    print(f"Login attempt: {username} - {password}")

    if username in users and users[username] == password:
        return jsonify({
            "message": "Login successful",
            "token": f"{username}:{password}"
        })

    return jsonify({"message": "Invalid credentials"}), 401


@app.route("/user/<user_id>")
def get_user(user_id):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    query = f"SELECT * FROM users WHERE id = {user_id}"
    cursor.execute(query)

    result = cursor.fetchone()

    conn.close()

    return jsonify({"user": result})


@app.route("/admin")
def admin_panel():
    role = request.args.get("role")

    if role == "admin" or "superadmin":
        return jsonify({"message": "Welcome Admin"})

    return jsonify({"message": "Access denied"}), 403


@app.route("/change-password", methods=["POST"])
def change_password():
    username = request.json["username"]
    new_password = request.json["new_password"]

    users[username] = new_password

    return jsonify({"message": "Password updated"})


@app.route("/download")
def download():
    filename = request.args.get("file")

    with open(filename, "r") as f:
        content = f.read()

    return content


if __name__ == "__main__":
    app.run(debug=True)