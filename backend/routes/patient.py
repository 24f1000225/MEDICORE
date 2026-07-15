from datetime import date, datetime
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.database import db
from backend.models.appointment import Appointment
from backend.models.doctor import Doctor
from backend.models.user import User
from backend.models.patient import Patient
from backend.models.availability import Availability
from backend.utils.auth import role_required
from flask_jwt_extended import get_jwt_identity


patient_bp = Blueprint("patient", __name__)

# patient doctors availability ko dehk sakta hai 
@patient_bp.route("/doctor-availability/<int:doctor_id>", methods=["GET"])
@jwt_required()
def doctor_availability(doctor_id):

    slots = Availability.query.filter_by(
        doctor_id=doctor_id,
        is_available=True
    ).all()

    result = []

    for s in slots:
        result.append({
            "date": s.date.strftime("%Y-%m-%d"),
            "time": s.time.strftime("%H:%M")
        })

    return jsonify(result)

# patient appointment book kar sakta hai 
@patient_bp.route("/book", methods=["POST"])
@jwt_required()
@role_required("patient")
def book_appointment():

    data = request.get_json()

    user_id = get_jwt_identity()

    patient = Patient.query.filter_by(user_id=user_id).first()

    if not patient:
        return jsonify({"error": "Patient profile not found"}), 404

    date_obj = datetime.strptime(data["date"], "%Y-%m-%d").date()
    time_obj = datetime.strptime(data["time"], "%H:%M").time()

    doctor_id = int(data["doctor_id"])

    existing = Appointment.query.filter_by(
        doctor_id=doctor_id,
        date=date_obj,
        time=time_obj
    ).first()

    if existing:
        return jsonify({"error": "Doctor already booked at this time"}), 400

    appointment = Appointment(
        doctor_id=doctor_id,
        patient_id=patient.id,
        date=date_obj,
        time=time_obj,
        status="Booked"
    )

    db.session.add(appointment)
    db.session.commit()

    return jsonify({"msg": "Appointment booked"})

# patient sari appointment ek jgha dehk sakta hai 
@patient_bp.route("/appointments", methods=["GET"])
@jwt_required()
@role_required("patient")
def get_appointments():

    user_id = get_jwt_identity()

    patient = Patient.query.filter_by(user_id=user_id).first()

    appointments = Appointment.query.filter_by(patient_id=patient.id).all()

    result = []

    for a in appointments:
        result.append({
            "id": a.id,
            "date": a.date.strftime("%Y-%m-%d"),
            "time": a.time.strftime("%H:%M"),
            "status": a.status,
            "diagnosis": a.diagnosis,
            "treatment": a.treatment,
            "prescription": a.prescription
        })

    return jsonify(result)

# patient appointment ko cancel kar sakta hai 
@patient_bp.route("/appointments/<int:id>", methods=["DELETE"])
@jwt_required()
@role_required("patient")
def cancel_appointment(id):

    appointment = Appointment.query.get_or_404(id)

    db.session.delete(appointment)

    db.session.commit()

    return {"msg": "Appointment cancelled"}

# patient ki appointment history
@patient_bp.route("/history", methods=["GET"])
@jwt_required()
@role_required("patient")
def appointment_history():

    user_id = get_jwt_identity()

    patient = Patient.query.filter_by(user_id=user_id).first()

    appointments = Appointment.query.filter_by(
        patient_id=patient.id,
        status = "Completed"
    ).all()

    result = []

    for a in appointments:

        if a.status == "completed":

            result.append({
                "id": a.id,
                "doctor_id": a.doctor_id,
                "date": a.date.strftime("%Y-%m-%d"),
                "time": a.time.strftime("%H:%M"),
                "diagnosis": a.diagnosis,
                "treatment": a.treatment,
                "prescription": a.prescription,
                "doctor_notes": a.doctor_notes
            })

    return jsonify(result)

# patient apni profile ko eddit kar skata hai 
@patient_bp.route("/profile", methods=["PUT"])
@jwt_required()
@role_required("patient")
def update_profile():

    user_id = get_jwt_identity()

    data = request.get_json()

    user = User.query.get(user_id)

    user.username = data.get("username", user.username)
    user.email = data.get("email", user.email)

    db.session.commit()

    return jsonify({"msg": "Profile updated"})

# export route
@patient_bp.route("/export", methods=["POST"])
@jwt_required()
def export_csv():
    from backend.tasks.export_csv import export_patient_treatments

    user_id = get_jwt_identity()

    export_patient_treatments.delay(user_id)

    return {"message": "Export started. You will be notified when it finishes."}

# paitent sare doctor ko dehk sakta hai 
@patient_bp.route("/doctors", methods=["GET"])
@jwt_required()
@role_required("patient")
def get_doctors():

    specialization = request.args.get("specialization")

    query = Doctor.query.join(User)

    if specialization:
        query = query.filter(
            Doctor.specialization.ilike(f"%{specialization}%")
        )

    doctors = query.all()

    result = []

    for doc in doctors:
        result.append({
            "id": doc.id,
            "username": doc.user.username,
            "email": doc.user.email,
            "specialization": doc.specialization,
            "department_id": doc.department_id
        })

    return jsonify(result)
