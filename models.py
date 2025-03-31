from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    date = db.Column(db.String(10), nullable=False)
    time = db.Column(db.String(5), nullable=False)


