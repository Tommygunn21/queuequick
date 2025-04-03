from flask import Flask, request, jsonify, render_template, redirect, url_for
from models import db
import logging

app = Flask(__name__)
app.config.from_pyfile('config.py')

# Initialize database
db.init_app(app)

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

