import os
from flask import Flask
from backend.database import db
from backend.models import User
from flask_jwt_extended import JWTManager
from backend.routes.auth import auth_bp
from backend.routes.admin import admin_bp
from backend.routes.doctor import doctor_bp
from backend.routes.patient import patient_bp
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    CORS(app)

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///hospital.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["JWT_SECRET_KEY"] = "hospital-management-system-secure-secret-key"

    db.init_app(app)
    jwt = JWTManager(app)

    with app.app_context():
        db.create_all()
        create_admin()
        

    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(admin_bp, url_prefix="/admin")
    app.register_blueprint(doctor_bp, url_prefix="/doctor")
    app.register_blueprint(patient_bp, url_prefix="/patient")

    return app


def create_admin():
    
    existing_admin = User.query.filter_by(role="admin").first()
    if not existing_admin:
        admin = User(
            username="admin",
            email="admin@medicore.com",
            role="admin"
            
        )
        admin.set_password("admin123")
        db.session.add(admin)
        db.session.commit()
        print("Admin created successfully.")


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)