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
    __SMTP_SERVER = 'smtp.gmail.com'
    __SMTP_PORT = 587
    __SENDER_EMAIL = 'philip.car.rental@gmail.com'  # Admin email
    __SENDER_PASSWORD = 'rgbw mikh hbvp wrrd'         # App password

    @staticmethod
    def send_email(to_email, subject, body, texts=None):
        """
        Send a generic email with the given subject and body to the specified recipient.
        Uses i18n texts for confirmation message if provided.
        """
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = EmailService.__SENDER_EMAIL
        msg['To'] = to_email
        try:
            server = smtplib.SMTP(EmailService.__SMTP_SERVER, EmailService.__SMTP_PORT)
            server.starttls()
            server.login(EmailService.__SENDER_EMAIL, EmailService.__SENDER_PASSWORD)
            server.sendmail(EmailService.__SENDER_EMAIL, [to_email], msg.as_string())
            server.quit()
            if texts and "EmailTexts" in texts and "email_sent" in texts["EmailTexts"]:
                print(texts["EmailTexts"]["email_sent"].format(to_email=to_email))
            else:
                print(f"Email sent to {to_email}")
        except Exception as e:
            print(f"Failed to send email: {e}")

    @staticmethod
    def send_approval_email(to_email, car_make, car_model, start_date, end_date, amount, texts):
        """
        Send an approval email using i18n texts.
        """
        subject = texts["EmailTexts"]["approval_subject"]
        body = texts["EmailTexts"]["approval_body"].format(
            car_make=car_make,
            car_model=car_model,
            start_date=start_date,
            end_date=end_date,
            amount=amount
        )
        EmailService.send_email(to_email, subject, body, texts)

    @staticmethod
    def send_rejection_email(to_email, car_make, car_model, start_date, end_date, texts):
        """
        Send a rejection email using i18n texts.
        """
        subject = texts["EmailTexts"]["rejection_subject"]
        body = texts["EmailTexts"]["rejection_body"].format(
            car_make=car_make,
            car_model=car_model,
            start_date=start_date,
            end_date=end_date
        )
        EmailService.send_email(to_email, subject, body, texts)
