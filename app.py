from flask import Flask, request, jsonify, render_template, redirect, url_for
from models import db
import logging

app = Flask(__name__)
app.config.from_pyfile('config.py')

# Initialize database
db.init_app(app)

@app.route('/cause-error')
def cause_error():
    raise Exception("Intentional test error from Elon")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/appointments', methods=['GET', 'POST'])
def appointments():
    if request.method == 'POST':
        # Example: handle booking
        data = request.form
        # You can add your booking logic here
        return redirect(url_for('appointments'))

    # Otherwise, return list of appointments (example data)
    example_appointments = [
        {"name": "Tom", "time": "10:00 AM"},
        {"name": "Lisa", "time": "10:30 AM"}
    ]
    return render_template('appointments.html', appointments=example_appointments)
from datetime import datetime, timedelta

# Temporary in-memory example appointment list
appointments = [
    {
        "id": 1,
        "client": "Tom",
        "time": datetime(2024, 4, 3, 10, 0),  # Tomorrow at 10:00 AM
    }
]

# Business policy configuration
business_policy = {
    "allow_reschedule": True,
    "reschedule_min_notice": 120,  # minutes
    "allow_late_notice": True,
    "late_grace_period": 10,       # minutes
}

@app.route('/reschedule/<int:appointment_id>', methods=['POST'])
def reschedule(appointment_id):
    appointment = next((a for a in appointments if a["id"] == appointment_id), None)
    if not appointment:
        return jsonify({"error": "Appointment not found"}), 404

    now = datetime.now()
    time_until_appt = (appointment["time"] - now).total_seconds() / 60

    if not business_policy["allow_reschedule"]:
        return jsonify({"error": "Rescheduling not allowed"}), 403

    if time_until_appt < business_policy["reschedule_min_notice"]:
        return jsonify({"error": f"Rescheduling must be at least {business_policy['reschedule_min_notice']} minutes in advance"}), 403

    # In real version: update appointment in DB
    return jsonify({"message": "Reschedule request received"}), 200

@app.route('/running-late/<int:appointment_id>', methods=['POST'])
def running_late(appointment_id):
    appointment = next((a for a in appointments if a["id"] == appointment_id), None)
    if not appointment:
        return jsonify({"error": "Appointment not found"}), 404

    now = datetime.now()
    minutes_late = (now - appointment["time"]).total_seconds() / 60

    if not business_policy["allow_late_notice"]:
        return jsonify({"error": "Late notice not allowed"}), 403

    if minutes_late > business_policy["late_grace_period"]:
        return jsonify({"error": "Too late to notify. Appointment may be marked as no-show."}), 403

    # In real version: flag appointment as 'late' in DB
    return jsonify({"message": "Late notice received"}), 200

# === GLOBAL ERROR HANDLING ===

# Set up logging
logging.basicConfig(level=logging.INFO)

@app.errorhandler(Exception)
def handle_exception(e):
    app.logger.error(f"Unhandled Exception: {str(e)}")
    return jsonify({"error": "Something went wrong on the server."}), 500

# === RUN FLASK ===
if __name__ == "__main__":
    app.run(port=5001, debug=True)

