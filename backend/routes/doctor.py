from datetime import datetime
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.database import db
from backend.models.doctor import Doctor
from backend.models.appointment import Appointment
from backend.models.treatment import Treatment
from backend.models.availability import Availability
from backend.utils.auth import role_required

doctor_bp = Blueprint("doctor", __name__)


@doctor_bp.route("/dashboard", methods=["GET"])
@role_required("doctor")
def doctor_dashboard():
    return jsonify({"msg": "Welcome Doctor"})

# doctors apni availability ko set kar sakta hai 
@doctor_bp.route("/availability", methods=["POST"])
@jwt_required()
@role_required("doctor")
def set_availability():

    data = request.get_json()

    user_id = get_jwt_identity()

    doctor = Doctor.query.filter_by(user_id=user_id).first()

    date_obj = datetime.strptime(data["date"], "%Y-%m-%d").date()
    time_obj = datetime.strptime(data["time"], "%H:%M").time()

    availability = Availability(
        doctor_id=doctor.id,
        date=date_obj,
        time=time_obj,
        is_available=True
    )

    db.session.add(availability)
    db.session.commit()

    return jsonify({"msg": "Availability added"})

# getDoctorAvailability
@doctor_bp.route("/availability", methods=["GET"])
@jwt_required()
@role_required("doctor")
def get_availability():

    user_id = get_jwt_identity()

    doctor = Doctor.query.filter_by(user_id=user_id).first()

    availability = Availability.query.filter_by(doctor_id=doctor.id).all()

    result = []

    for a in availability:
        result.append({
            "id": a.id,
            "date": a.date.strftime("%Y-%m-%d"),
            "time": a.time.strftime("%H:%M"),
            "is_available": a.is_available
        })

    return jsonify(result)

# doctor appointments dehk sakta hai 
@doctor_bp.route("/appointments", methods=["GET"])
@jwt_required()
@role_required("doctor")
def get_appointments():

    user_id = get_jwt_identity()

    doctor = Doctor.query.filter_by(user_id=user_id).first()

    appointments = Appointment.query.filter_by(doctor_id=doctor.id).all()

    result = []

    for a in appointments:
        result.append({
            "id": a.id,
            "patient_id": a.patient_id,
            "date": a.date.strftime("%Y-%m-%d"),
            "time": a.time.strftime("%H:%M"),
            "status": a.status,
            "diagnosis": a.diagnosis,
            "treatment": a.treatment,
            "prescription": a.prescription
        })
    return jsonify(result)

# doctor completed appointment ko mark kar sakta hai 
# appointment hone ke baad ka status 
@doctor_bp.route("/appointments/<int:appointment_id>/complete", methods=["PUT"])
@jwt_required()
@role_required("doctor")
def complete_appointment(appointment_id):

    appointment = Appointment.query.get_or_404(appointment_id)

    appointment.status = "Completed"

    db.session.commit()

    return jsonify({"msg": "Appointment marked completed"})

# appointment ke status
# appointment hone se phele ka status 
@doctor_bp.route("/appointments/<int:id>", methods=["PUT"])
@jwt_required()
@role_required("doctor")
def update_appointment(id):

    data = request.get_json()

    appointment = Appointment.query.get_or_404(id)

    appointment.status = data["status"]

    db.session.commit()

    return {"msg": "Appointment updated"}

# doctor treatment ko add kar sakta hai 
@doctor_bp.route("/treatment", methods=["POST"])
@jwt_required()
@role_required("doctor")
def add_treatment():

    data = request.get_json()

    treatment = Treatment(
        appointment_id=data["appointment_id"],
        diagnosis=data["diagnosis"],
        prescription=data["prescription"]
    )

    db.session.add(treatment)
    db.session.commit()

    return jsonify({"msg": "Treatment added"})

# doctor treatment ko update kar sakta hai
@doctor_bp.route("/treatment/<int:appointment_id>", methods=["PUT"])
@jwt_required()
@role_required("doctor")
def update_treatment(appointment_id):

    data = request.get_json()

    appointment = Appointment.query.get_or_404(appointment_id)

    appointment.diagnosis = data.get("diagnosis")
    appointment.treatment = data.get("treatment")
    appointment.prescription = data.get("prescription")
    appointment.doctor_notes = data.get("doctor_notes")

    appointment.status = "completed"

    db.session.commit()

    return jsonify({"msg": "Treatment updated"})

# doctor patient ki histor dehk sakta hai
@doctor_bp.route("/patient-history/<int:patient_id>", methods=["GET"])
@jwt_required()
@role_required("doctor")
def patient_history(patient_id):

    appointments = Appointment.query.filter_by(
        patient_id=patient_id,
        status="completed"
    ).all()

    result = []

    for a in appointments:
        result.append({
            "appointment_id": a.id,
            "date": a.date.strftime("%Y-%m-%d"),
            "time": a.time.strftime("%H:%M"),
            "diagnosis": a.diagnosis,
            "treatment": a.treatment,
            "prescription": a.prescription,
            "doctor_notes": a.doctor_notes
        })

    return jsonify(result)

@doctor_bp.route("/appointments/<int:id>/status", methods=["PUT"])
@jwt_required()
@role_required("doctor")
def update_status(id):

    data = request.get_json()

    appointment = Appointment.query.get_or_404(id)

    appointment.status = data["status"]

    db.session.commit()

    return jsonify({"msg": "Status updated"})

