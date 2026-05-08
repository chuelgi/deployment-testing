import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Get database URL from Render environment variables
database_url = os.getenv("DATABASE_URL")

# Fix Render postgres URL if needed
if database_url and database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)

# Configure SQLAlchemy
app.config["SQLALCHEMY_DATABASE_URI"] = database_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# Example model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)


# Create tables automatically on startup
with app.app_context():
    db.create_all()

@app.route("/")
def home():
    return "<p>Hello this is the home page</p>"

@app.route("/create")
def create():
    user = User(username="alex")
    db.session.add(user)
    db.session.commit()
    return "User created"

@app.route("/users")
def users():
    all_users = User.query.all()
    return "<br>".join([u.username for u in all_users])

if __name__ == "__main__":
    app.run(debug=True)