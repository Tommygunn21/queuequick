from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

# Initialize Flask app
app = Flask(__name__)

# Database configuration using Render's DATABASE_URL
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
from models import db
db.init_app(app)

# Initialize Flask-Migrate
migrate = Migrate(app, db)

# Route to render homepage
@app.route('/')
def home():
    return render_template('index.html')

# Route to display all appointments (sample future functionality)
@app.route('/appointments')
def appointments():
    from models import Appointment
    all_appointments = Appointment.query.all()
    return render_template('appointments.html', appointments=all_appointments)

# Route for adding sample appointment (temporary for testing)
@app.route('/add_sample')
def add_sample():
    from models import Appointment
    new_appointment = Appointment(customer_name='John Doe', appointment_time='2025-04-05 10:00:00')
    db.session.add(new_appointment)
    db.session.commit()
    return "Sample appointment added!"

# Run the app if launched directly
if __name__ == '__main__':
    app.run(debug=False)



