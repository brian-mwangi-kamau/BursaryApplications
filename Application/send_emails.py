import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr
from dotenv import load_dotenv
from .models import Application
from .views import send_to_mail

load_dotenv()

smtp_server = os.environ['smtp_server']
smtp_port = os.environ['smtp_port']
sender_email = os.environ['sender_email']
sender_password = os.environ['sender_password']
recipient_email = os.environ['recipient_email']

def main():
    applications = Application.objects.all()
    send_to_mail(applications)

if __name__ == '__main__':
    main()
