from backend.database import db
from sqlalchemy import UniqueConstraint

class Appointment(db.Model):

    __tablename__ = "appointments"
    id = db.Column(db.Integer, primary_key=True)
    doctor_id = db.Column(db.Integer,db. ForeignKey("doctors.id"), nullable=False)
    patient_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    status = db.Column(db.String(20), default="pending")
    diagnosis = db.Column(db.Text)
    treatment = db.Column(db.Text)
    prescription = db.Column(db.Text)
    doctor_notes = db.Column(db.Text)
    doctor = db.relationship("Doctor", backref="appointments")
    patient = db.relationship("User", backref="appointments")