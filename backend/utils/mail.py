import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def send_email(receiver_email, subject, html_body):

    sender_email = "hospitalproject@gmail.com"
    app_password = "hbhvoqnalpxzbdth"

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = receiver_email

    html_part = MIMEText(html_body, "html")
    msg.attach(html_part)

    try:

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()

        server.login(sender_email, app_password)

        server.sendmail(sender_email, receiver_email, msg.as_string())

        server.quit()

        print("Email sent to:", receiver_email)

    except Exception as e:

        print("Email sending failed:", e)