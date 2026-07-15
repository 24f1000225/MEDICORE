from datetime import date
from backend.celery_worker import celery
from backend.models.appointment import Appointment
from backend.utils.mail import send_email
from main import create_app

app = create_app()

@celery.task
def send_daily_reminders():
    with app.app_context():
        today = date.today()
        appointments = Appointment.query.filter_by(date=today).all()
        for appt in appointments:
            patient = appt.patient.user
            subject = "Hospital Appointment Reminder"
            message = f"""
            Hello {patient.username},
            This is a reminder that you have an appointment today.
            Doctor: {appt.doctor.user.username}
            Time: {appt.time}
            Please visit the hospital on time.
            Thank you
            """
            send_email(patient.email, subject, message)
        return "Reminders sent"