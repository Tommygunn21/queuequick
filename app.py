from flask import Flask, render_template
from models import db
import os

app = Flask(__name__)

# Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL').replace("postgres://", "postgresql://", 1)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize Database
db.init_app(app)

# Create Tables if they don't exist
with app.app_context():
    db.create_all()

# Home Route
@app.route('/')
def home():
    return render_template('index.html')

# Example Route (optional)
@app.route('/book')
def book():
    return "Booking Page Placeholder"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)



