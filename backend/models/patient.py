from backend.database import db

class Patient(db.Model):
    __tablename__ = "patients"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    age = db.Column(db.Integer)
    gender = db.Column(db.String(10))
    phone = db.Column(db.String(20))
    
    user = db.relationship("User", backref="patient_profile", uselist=False)