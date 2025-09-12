"""
email_service.py

Service layer for sending email notifications in the car rental system.
Provides methods to send approval and rejection emails to customers using SMTP.
"""

import smtplib
from email.mime.text import MIMEText

class EmailService:
    """
    Service class for handling email notifications.
    Uses SMTP to send emails for booking approvals and rejections.
    """
    SMTP_SERVER = 'smtp.gmail.com'
    SMTP_PORT = 587
    SENDER_EMAIL = 'philip.car.rental@gmail.com'  # Admin email
    SENDER_PASSWORD = 'rgbw mikh hbvp wrrd'         # App password

    @staticmethod
    def send_email(to_email, subject, body):
        """
        Send a generic email with the given subject and body to the specified recipient.
        """
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = EmailService.SENDER_EMAIL
        msg['To'] = to_email
        try:
            server = smtplib.SMTP(EmailService.SMTP_SERVER, EmailService.SMTP_PORT)
            server.starttls()
            server.login(EmailService.SENDER_EMAIL, EmailService.SENDER_PASSWORD)
            server.sendmail(EmailService.SENDER_EMAIL, [to_email], msg.as_string())
            server.quit()
            print(f"Email sent to {to_email}")
        except Exception as e:
            print(f"Failed to send email: {e}")

    @staticmethod
    def send_approval_email(to_email, car_id, start_date, end_date, amount):
        """
        Send an approval email to the customer for a successful car rental booking.
        """
        subject = "Philip Rent-A-Car: Your Car Rental Has Been Approved"
        body = f"Your booking for car ID {car_id} from {start_date} to {end_date} has been approved. The total amount is ${amount}. Due upon pickup."
        EmailService.send_email(to_email, subject, body)

    @staticmethod
    def send_rejection_email(to_email, car_id, start_date, end_date):
        """
        Send a rejection email to the customer for a declined car rental booking.
        """
        subject = "Philip Rent-A-Car: Your Car Rental Has Been Rejected"
        body = f"Your booking for car ID {car_id} from {start_date} to {end_date} has been rejected."
        EmailService.send_email(to_email, subject, body)
