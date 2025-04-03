from flask import Flask, request, jsonify, render_template, redirect, url_for
from datetime import datetime
import logging

app = Flask(__name__)

# In-memory appointment list
appointments = [
    {
        "id": 1,
        "client": "Tom",
        "time": datetime(2025, 4, 3, 10, 0),  # Example future time
        "status": "booked"
    }
]

# Client score tracking
clients = {
    "Tom": {
        "score": "green",
        "late_count": 0,
        "no_show_count": 0
    }
}

# Business policy config
business_policy = {
    "allow_reschedule": True,
    "reschedule_min_notice": 120,  # minutes
    "allow_late_notice": True,
    "late_grace_period": 10,       # minutes
}

# Score update logic
def update_client_score(client_name):
    client = clients.get(client_name)
    if not client:
        clients[client_name] = {
            "score": "green",
            "late_count": 0,
            "no_show_count": 0
        }
        client = clients[client_name]

    late = client["late_count"]
    no_show = client["no_show_count"]

    if no_show >= 3 or late >= 5:
        client["score"] = "red"
    elif no_show >= 1 or late >= 2:
        client["score"] = "yellow"
    else:
        client["score"] = "green"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/appointments', methods=['GET', 'POST'])
def appointments_view():
    if request.method == 'POST':
        client_name = request.form.get("client", "Unknown")
        appointment_time = datetime.now()
        new_id = len(appointments) + 1
        appointments.append({
            "id": new_id,
            "client": client_name,
            "time": appointment_time,
            "status": "booked"
        })
        if client_name not in clients:
            clients[client_name] = {
                "score": "green",
                "late_count": 0,
                "no_show_count": 0
            }
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
        return jsonify({"error": "Rescheduling not allowed"}),

