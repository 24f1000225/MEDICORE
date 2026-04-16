from backend.database import db

class Treatment(db.Model):
    __tablename__ = "treatments"

    id = db.Column(db.Integer, primary_key=True)
    appointment_id = db.Column(db.Integer, db.ForeignKey("appointments.id"), nullable=False)
    diagnosis = db.Column(db.Text)
    prescription = db.Column(db.Text)
    notes = db.Column(db.Text)