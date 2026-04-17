from flask import Blueprint, request, jsonify
from backend.database import db
from backend.models import User, Patient
from flask_jwt_extended import create_access_token
from datetime import timedelta

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register/patient", methods=["POST"])
def register_patient():

    data = request.get_json()

    # create user
    new_user = User(
        username=data["username"],
        email=data["email"],
        role="patient"
    )

    new_user.set_password(data["password"])

    db.session.add(new_user)
    db.session.flush()


    # create patient profile
    patient = Patient(
        user_id=new_user.id
    )

    db.session.add(patient)
    db.session.commit()

    return jsonify({
        "msg": "Patient registered successfully"
    }), 201

@auth_bp.route("/login", methods=["POST"])
def login():

    data = request.get_json()

    if not data or "username" not in data or "password" not in data:
        return jsonify({"message": "Missing credentials"}), 400

    user = User.query.filter_by(username=data["username"]).first()

    # check if user exists
    if not user:
        return jsonify({"message": "Invalid credentials"}), 401

    # blacklist check
    if not user.is_active:
        return jsonify({"msg": "Account has been blacklisted"}), 403

    # password check
    if not user.check_password(data["password"]):
        return jsonify({"message": "Invalid credentials"}), 401

    token = create_access_token(
        identity=str(user.id),
        additional_claims={"role": user.role},
        expires_delta=timedelta(hours=2)
    )

    return jsonify({
        "token": token,
        "role": user.role
    }), 200