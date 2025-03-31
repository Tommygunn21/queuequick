from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate  # <-- Add this!
from config import Config
from models import db, Appointment

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

# Add this to enable Flask-Migrate
migrate = Migrate(app, db)

# Homepage route
@app.route('/')
def home():
    return render_template('index.html')

# Route to book an appointment
@app.route('/book', methods=['GET', 'POST'])
def book_appointment():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        date = request.form['date']
        time = request.form['time']

        # Create new appointment and save it to the database
        new_appointment = Appointment(name=name, email=email, date=date, time=time)
        db.session.add(new_appointment)
        db.session.commit()

        return redirect(url_for('success'))

    return render_template('book.html')

# Success route
@app.route('/success')
def success():
    return render_template('success.html')

# Route to manage appointments
@app.route('/manage')
def manage_appointments():
    appointments = Appointment.query.all()
    return render_template('manage.html', appointments=appointments)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)

