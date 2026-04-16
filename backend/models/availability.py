from backend.database import db

class Availability(db.Model):
    __tablename__ = "Availability"

    id = db.Column(db.Integer, primary_key=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey("doctors.id"))
    date = db.Column(db.Date)
    time = db.Column(db.Time)
    is_available = db.Column(db.Boolean, default=True)