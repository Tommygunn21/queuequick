from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(100), nullable=False)
    appointment_time = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(20), default='pending')


