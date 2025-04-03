from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import logging
import os

app = Flask(__name__)

# === CONFIG ===
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://queuequick_db_user:u5JfurFSEpaXSQVCLh8jFKGkkdejUXUL@dpg-cvkt8qadbo4c73fb6pmg-a/queuequick_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# === MODELS ===
class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    score = db.Column(db.String(10), default="green")
    late_count = db.Column(db.Integer, default=0)
    no_show_count = db.Column(db.Integer, default=0)

class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=False)
    time = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(20), default="booked")
    client = db.relationship('Client', backref=db.backref('appointments', lazy=True))

# === BUSINESS POLICY ===
business_policy = {
    "allow_reschedule": True,
    "reschedule_min_notice": 120,  # minutes
    "allow_late_notice": True,
    "late_grace_period": 10       # minutes
}

# === SCORE LOGIC ===
def update_client_score(client):
    if client.no_show_count >= 3 or client.late_count >= 5:
        client.score = "red"
    elif client.no_show_count >= 1 or client.late_count >= 2:
        client.score = "yellow"
    else:
        client.score = "green"

# === ROUTES ===
@app.route('/init-db')
def init_db():
    db.create_all()
    return jsonify({"message": "Database tables created"})
@app.route("/appointments", methods=["POST"])
def create_appointment():
    name = request.json.get("client")
    time_str = request.json.get("time")
    appt_time = datetime.strptime(time_str, "%Y-%m-%d %H:%M")

    client = Client.query.filter_by(name=name).first()
    if not client:
        client = Client(name=name)
        db.session.add(client)
        db.session.commit()

    appt = Appointment(client_id=client.id, time=appt_time)
    db.session.add(appt)
    db.session.commit()

    return jsonify({"message": "Appointment created", "id": appt.id}), 201

@app.route("/reschedule/<int:appointment_id>", methods=["POST"])
def reschedule(appointment_id):
    appt = Appointment.query.get(appointment_id)
    if not appt:
        return jsonify({"error": "Appointment not found"}), 404

    now = datetime.now()
    time_until = (appt.time - now).total_seconds() / 60
    if not business_policy["allow_reschedule"] or time_until < business_policy["reschedule_min_notice"]:
        return jsonify({"error": "Rescheduling not allowed under policy"}), 403

    appt.status = "rescheduled"
    update_client_score(appt.client)
    db.session.commit()
    return jsonify({"message": "Rescheduled", "status": appt.status})

@app.route("/running-late/<int:appointment_id>", methods=["POST"])
def running_late(appointment_id):
    appt = Appointment.query.get(appointment_id)
    if not appt:
        return jsonify({"error": "Appointment not found"}), 404

    now = datetime.now()
    minutes_late = (now - appt.time).total_seconds() / 60
    if not business_policy["allow_late_notice"] or minutes_late > business_policy["late_grace_period"]:
        return jsonify({"error": "Too late to notify"}), 403

    appt.status = "late"
    appt.client.late_count += 1
    update_client_score(appt.client)
    db.session.commit()

    return jsonify({"message": "Late notice recorded", "status": appt.status})

@app.route("/clients", methods=["GET"])
def get_clients():
    all_clients = Client.query.all()
    return jsonify({c.name: {
        "score": c.score,
        "late_count": c.late_count,
        "no_show_count": c.no_show_count
    } for c in all_clients})

# === ERROR HANDLING ===
logging.basicConfig(level=logging.INFO)
@app.errorhandler(Exception)
def handle_error(e):
    app.logger.error(f"Unhandled Exception: {str(e)}")
    return jsonify({"error": "Something went wrong on the server."}), 500

# === INIT ===
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(port=5001, debug=True)

