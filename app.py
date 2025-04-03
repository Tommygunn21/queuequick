from flask import Flask, request, jsonify, render_template, redirect, url_for
from datetime import datetime
import logging

app = Flask(__name__)

# Dummy database (in-memory for now)
appointments = [
    {
        "id": 1,
        "client": "Tom",
        "time": datetime(2024, 4, 3, 10, 0),  # Example date
        "status": "booked"
    }
]

# Business policy configuration
business_policy = {
    "allow_reschedule": True,
    "reschedule_min_notice": 120,  # minutes
    "allow_late_notice": True,
    "late_grace_period": 10,       # minutes
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/appointments', methods=['GET', 'POST'])
def appointments_view():
    if request.method == 'POST':
        # Handle new appointment (placeholder)
        client_name = request.form.get("client", "Unknown")
        appointment_time = datetime.now()
        new_id = len(appointments) + 1
        appointments.append({
            "id": new_id,
            "client": client_name,
            "time": appointment_time,
            "status": "booked"
        })
        return redirect(url_for('appointments_view'))

    return render_template('appointments.html', appointments=appointments)

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

    appointment["status"] = "rescheduled"

    return jsonify({
        "message": "Reschedule request received",
        "appointment": {
            "id": appointment["id"],
            "client": appointment["client"],
            "status": appointment["status"]
        }
    }), 200

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

    appointment["status"] = "late"

    return jsonify({
        "message": "Late notice received",
        "appointment": {
            "id": appointment["id"],
            "client": appointment["client"],
            "status": appointment["status"]
        }
    }), 200

# Set up logging
logging.basicConfig(level=logging.INFO)

@app.errorhandler(Exception)
def handle_exception(e):
    app.logger.error(f"Unhandled Exception: {str(e)}")
    return jsonify({"error": "Something went wrong on the server."}), 500

# Run locally
if __name__ == "__main__":
    app.run(port=5001, debug=True)

