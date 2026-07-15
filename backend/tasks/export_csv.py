import csv
import os

from backend.celery_worker import celery
from backend.models.appointment import Appointment
from backend.models.user import User
from main import create_app

app = create_app()


@celery.task
def export_patient_treatments(patient_id):

    with app.app_context():

        patient = User.query.get(patient_id)

        appointments = Appointment.query.filter_by(
            patient_id=patient_id
        ).all()

        folder = "backend/exports"

        os.makedirs(folder, exist_ok=True)

        file_path = f"{folder}/patient_{patient_id}_treatments.csv"

        with open(file_path, "w", newline="") as file:

            writer = csv.writer(file)

            writer.writerow([
                "user_id",
                "username",
                "doctor",
                "appointment_date",
                "diagnosis",
                "treatment",
                "prescription",
                "next_visit"
            ])

            for appt in appointments:

                writer.writerow([
                    appt.patient_id,
                    patient.username,
                    appt.doctor.user.username,
                    appt.date,
                    appt.diagnosis,
                    appt.treatment,
                    appt.prescription,
                    appt.next_visit
                ])

        print("CSV Export Completed:", file_path)

        return file_path