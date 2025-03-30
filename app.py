from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from models import db
from config import Config

app = Flask(__name__)
# Load configuration
app.config.from_object(Config)

# Initialize the database
db.init_app(app)

# Create tables before the first request
with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return "QueueQuick is Live!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=False)


