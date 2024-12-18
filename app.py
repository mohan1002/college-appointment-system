from flask import Flask, request, jsonify
from models import db, User, Availability, Appointment

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///college.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

@app.route('/auth/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(email=data['email']).first()
    if user and user.password_hash == data['password']:  # Simple check for learning purposes
        return jsonify({"message": "Login successful", "user_id": user.id, "role": user.role})
    return jsonify({"message": "Invalid credentials"}), 401

@app.route('/professors/<int:professor_id>/availability', methods=['POST'])
def add_availability(professor_id):
    data = request.json
    slot = Availability(professor_id=professor_id, start_time=data['start_time'], end_time=data['end_time'])
    db.session.add(slot)
    db.session.commit()
    return jsonify({"message": "Availability added", "slot_id": slot.id})

@app.route('/appointments', methods=['POST'])
def book_appointment():
    data = request.json
    slot = Availability.query.get(data['slot_id'])
    if slot and slot.status == 'Available':
        appointment = Appointment(professor_id=slot.professor_id, student_id=data['student_id'], slot_id=slot.id)
        slot.status = 'Booked'
        db.session.add(appointment)
        db.session.commit()
        return jsonify({"message": "Appointment booked", "appointment_id": appointment.id})
    return jsonify({"message": "Slot unavailable"}), 400
