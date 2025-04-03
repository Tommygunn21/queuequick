# Elon was here – test deploy
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from config import Config
from models import db, Appointment

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

# Homepage route
@app.route('/')
def home():
    return render_template('index.html')

# Route to book an appointment
@app.route('/book', methods=['GET', 'POST'])
def book_appointment():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        date = request.form.get('date')
        time = request.form.get('time')

        if not name or not email or not date or not time:
            flash('Please fill in all fields.', 'danger')
            return redirect(url_for('book_appointment'))

        try:
            # Create new appointment and save it to the database
            new_appointment = Appointment(name=name, email=email, date=date, time=time)
            db.session.add(new_appointment)
            db.session.commit()
            flash('Appointment booked successfully!', 'success')
            return redirect(url_for('success'))

        except Exception as e:
            flash('An error occurred while booking the appointment. Please try again.', 'danger')
            return redirect(url_for('book_appointment'))

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


