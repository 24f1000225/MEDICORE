from backend.database import db

class Doctor(db.Model):
    __tablename__ = "doctors"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey("departments.id"))
    specialization = db.Column(db.String(100))
    availability = db.Column(db.Text)

    user = db.relationship("User", backref="doctor_profile", uselist=False)  
