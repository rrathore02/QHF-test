# modules/email_sender.py

import smtplib
from email.message import EmailMessage
import os
import ssl
from dotenv import load_dotenv

# Load .env variables
load_dotenv()

SENDER_EMAIL = os.getenv("qhf.project01@gmail.com")
APP_PASSWORD = os.getenv("wjzc fasi eleg cguk")

def send_welcome_email(to_email, name):
    subject = "🎉 You've Subscribed to QHF Updates!"
    body = (
        f"Hi {name},\n\n"
        "Thank you for using the QHF tool!\n\n"
        "You've been successfully subscribed to receive email notifications when new versions are released.\n\n"
        "If you have any questions, feel free to reply to this email.\n\n"
        "Best regards,\nThe QHF Team"
    )

    msg = EmailMessage()
    msg['From'] = SENDER_EMAIL
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.set_content(body)

    try:
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(SENDER_EMAIL, APP_PASSWORD)
            smtp.send_message(msg)
        print(f"📧 Welcome email sent to {to_email}")
    except Exception as e:
        print(f"⚠️ Failed to send email to {to_email}: {e}")
