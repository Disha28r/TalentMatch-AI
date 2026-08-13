import os
import smtplib

from dotenv import load_dotenv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

load_dotenv()

def send_interview_email(
    receiver_email,
    candidate_name,
    interview_date,
    interview_time,
    interview_mode
):
        sender_email = os.getenv("EMAIL_ADDRESS")
        app_password = os.getenv("EMAIL_APP_PASSWORD")

        subject = "Interview Invitation - TalentMatch AI"

        body = f"""
Hello {candidate_name},

Congratulations!

You have been shortlisted for the next stage of our recruitment process.

Interview Details

📅 Date: {interview_date}

🕒 Time: {interview_time}

💻 Mode: {interview_mode}

Please be available 10 minutes before your scheduled interview.

Best Regards,

TalentMatch AI
"""

        message = MIMEMultipart()

        message["From"] = sender_email
        message["To"] = receiver_email
        message["Subject"] = subject

        message.attach(MIMEText(body, "plain"))

        try:
            with smtplib.SMTP("smtp.gmail.com", 587) as server:

                server.starttls()

                server.login(sender_email, app_password)

                server.send_message(message)
                
            return True
        except Exception as e:
            return str(e)