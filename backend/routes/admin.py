from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from backend.database import db
from backend.models import User, Doctor, Patient, Appointment, Department, doctor
from backend.utils.auth import role_required
from backend.utils.cache import get_cache, set_cache
from werkzeug.security import generate_password_hash

admin_bp = Blueprint("admin", __name__)

#dashboard entry page
@admin_bp.route("/dashboard", methods=["GET"])
@jwt_required()
@role_required("admin")
def dashboard():
    cache = get_cache("admin_stats")

    if cache:
        return jsonify(cache)

    stats = {
        "total_doctors": Doctor.query.count(),
        "total_patients": Patient.query.count(),
        "total_appointments": Appointment.query.count()
    }

    set_cache("admin_stats", stats, expiry=120)

    return jsonify(stats)

#createDoctor
@admin_bp.route("/doctors", methods=["POST"])
@jwt_required()
@role_required("admin")
def create_doctor():

    data = request.get_json()

    new_user = User(
        username=data["username"],
        email=data["email"],
        role="doctor"
    )

    new_user.set_password(data["password"])

    db.session.add(new_user)
    db.session.commit()

    new_doctor = Doctor(
        user_id=new_user.id,
        specialization=data.get("specialization"),
        department_id=int(data.get("department_id"))
    )

    db.session.add(new_doctor)
    db.session.commit()

    set_cache("doctors_list", None, expiry=0)

    return jsonify({"msg": "Doctor created successfully"}), 201

#updateDoctor
@admin_bp.route("/doctors/<int:id>", methods=["PUT"])
@jwt_required()
@role_required("admin")
def update_doctor(id):
    data = request.get_json()
    doctor = Doctor.query.get_or_404(id)

    doctor.specialization = data.get("specialization")
    doctor.department_id = data.get("department_id")
    doctor.user.username = data.get("username")
    doctor.user.email = data.get("email")

    db.session.commit()
    return jsonify({"message": "Doctor updated"})

# admin doctor ko delete kar sakta hai 
@admin_bp.route("/delete-doctors/<int:doctor_id>", methods=["DELETE"])
@jwt_required()
@role_required("admin")
def delete_doctor(doctor_id):

    doctor = Doctor.query.get_or_404(doctor_id)

    user = User.query.get(doctor.user_id)

    db.session.delete(doctor)
    db.session.delete(user)

    db.session.commit()

    return jsonify({"msg": "Doctor deleted"})

#BlacklistUser
@admin_bp.route("/blacklist/<int:user_id>", methods=["PUT"])
@jwt_required()
@role_required("admin")
def blacklist_user(user_id):
    user = User.query.get_or_404(user_id)

    user.is_active = False
    db.session.commit()

    return jsonify({"msg": "User blacklisted"})

# admin upcoming appointment dehk sakta hai
@admin_bp.route("/appointments", methods=["GET"])
@jwt_required()
@role_required("admin")
def view_appointments():
    appointments = Appointment.query.all()
    result = []
    for appt in appointments:
        result.append({
            "id": appt.id,
            "doctor": appt.doctor.user.username if appt.doctor else "Unknown",
            "patient": appt.patient.username if appt.patient else "Unknown",
            "date": appt.date.strftime("%Y-%m-%d"),
            "time": appt.time.strftime("%H:%M"),
            "status": appt.status,
            "diagnosis": appt.diagnosis,
            "treatment": appt.treatment,
            "prescription": appt.prescription
        })
    return jsonify(result)

# admin sare doctor ko dehk sakta hai
@admin_bp.route("/doctors", methods=["GET"])
@jwt_required()
def get_doctors():

    cached_data = get_cache("doctors_list")

    if cached_data:
        return jsonify(cached_data)

    doctors = Doctor.query.all()

    result = []

    for doctor in doctors:

        result.append({
            "id": doctor.id,
            "user_id": doctor.user_id,
            "username": doctor.user.username,
            "email": doctor.user.email,
            "specialization": doctor.specialization,
            "department_id": doctor.department_id
        })

    set_cache("doctors_list", result, expiry=5)

    return jsonify(result)

# admin sare paitent ki information dehk sakta hai
@admin_bp.route("/patients", methods=["GET"])
@jwt_required()
@role_required("admin")
def get_patients():
    patients = Patient.query.all()
    result = []
    for patient in patients:
        result.append({
            "id": patient.id,
            "username": patient.user.username,
            "email": patient.user.email,
            "user_id": patient.user_id
        })
    return jsonify(result)

# ek hi doctor ki profile ko update karne ke liye 
@admin_bp.route("/doctors/<int:id>", methods=["GET"])
@jwt_required()
@role_required("admin")
def get_doctor(id):

    doctor = Doctor.query.get_or_404(id)

    return jsonify({

        "id": doctor.id,

        "username": doctor.user.username,

        "email": doctor.user.email,

        "specialization": doctor.specialization,

        "department_id": doctor.department_id

    })


#searchDoctors
@admin_bp.route("/search/doctors", methods=["GET"])
@jwt_required()
@role_required("admin")
def search_doctors():
    query = request.args.get("q", "")
    doctors = Doctor.query.join(User).filter(
        (User.username.ilike(f"%{query}%")) |
        (Doctor.specialization.ilike(f"%{query}%"))
    ).all()
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

#searchPatients
@admin_bp.route("/search/patients", methods=["GET"])
@jwt_required()
@role_required("admin")
def search_patients():
    query = request.args.get("q", "")
    patients = Patient.query.join(User).filter(
        User.username.ilike(f"%{query}%")|
        User.email.ilike(f"%{query}%")|
        Patient.id.ilike(f"%{query}%")
    ).all()
    result = []
    for patient in patients:
        result.append({
            "id": patient.id,
            "username": patient.user.username,
            "email": patient.user.email
        })
    return jsonify(result)
