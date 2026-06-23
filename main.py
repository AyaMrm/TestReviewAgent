from flask import Flask
from auth import login, change_password

app = Flask(__name__)


@app.route("/")
def home():
    return "Auth API Running"


@app.route("/login", methods=["POST"])
def login_route():
    return login()


@app.route("/change-password", methods=["POST"])
def change_password_route():
    return change_password()


if __name__ == "__main__":
    app.run(debug=True)