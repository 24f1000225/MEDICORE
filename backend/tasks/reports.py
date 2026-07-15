from backend.celery_worker import celery
from backend.models.doctor import Doctor
from backend.models.appointment import Appointment
from backend.models.user import User
from backend.utils.mail import send_email
from main import create_app

from datetime import datetime, timedelta

app = create_app()


@celery.task
def send_monthly_reports():

    with app.app_context():

        today = datetime.today()

        # Calculate last month
        first_day_this_month = datetime(today.year, today.month, 1)
        last_month_end = first_day_this_month - timedelta(days=1)
        last_month_start = datetime(last_month_end.year, last_month_end.month, 1)

        doctors = Doctor.query.all()

        for doctor in doctors:

            user = User.query.get(doctor.user_id)

            appointments = Appointment.query.filter(
                Appointment.doctor_id == doctor.id,
                Appointment.date >= last_month_start,
                Appointment.date <= last_month_end
            ).all()

            html_report = f"""
            <h2>Monthly Activity Report</h2>

            <p><b>Doctor:</b> {user.username}</p>
            <p><b>Total Appointments:</b> {len(appointments)}</p>

            <table border="1" cellpadding="6">
            <tr>
                <th>Date</th>
                <th>Patient ID</th>
                <th>Diagnosis</th>
                <th>Treatment</th>
                <th>Prescription</th>
            </tr>
            """

            for a in appointments:

                html_report += f"""
                <tr>
                    <td>{a.date}</td>
                    <td>{a.patient_id}</td>
                    <td>{a.diagnosis}</td>
                    <td>{a.treatment}</td>
                    <td>{a.prescription}</td>
                </tr>
                """

            html_report += "</table>"

            send_email(
                user.email,
                "Monthly Hospital Activity Report",
                html_report
            )
            # Simulate sending email
            print("\n==============================")
            print("Monthly Report Sent To:", user.email)
            print(html_report)
            print("==============================\n")

