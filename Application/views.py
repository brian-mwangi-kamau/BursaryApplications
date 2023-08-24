import os
from django.shortcuts import render, redirect
#from .models import SiteSettings
from .forms import ApplicationForm
from .models import Application
from .models import VoterDatabase
 
# Imports for email functionality
import smtplib
from django.core.mail import send_mail
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr
from dotenv import load_dotenv
load_dotenv()

# Create your views here.
def application_form(request):
    if request.method == 'POST':
        form = ApplicationForm(request.POST)
        if form.is_valid():
            form_data = form.cleaned_data
            application = Application(
                student_name=form_data['student_name'],
                school_name=form_data['school_name'],
                admission_number=form_data['admission_number'],
                year_of_study=form_data['year_of_study'],
                constituency=form_data['constituency'],
                location=form_data['location'],
                phone_number=form_data['phone_number'],
                id_number=form_data['id_number']
            )
            application.save()
            return render(request, 'success.html')
    else:
        form = ApplicationForm()

    return render(request, 'Application.html', {'form': form})


def success(request):
    return render(request, 'success.html')



# View for Comparison
def process_applications():
    external_data = VoterDatabase.objects.using('external_database').all()

    to_spreadsheets = []
    manual_review = []

    for app in Application.objects.all():
        if app.id_number in external_data and \
           app.constituency == external_data[app.id_number]['constituency'] and \
           app.location == external_data[app.id_number]['location']:
            to_spreadsheets.append(app) # This will happen with the logic for sheets working
        else:
            manual_review.append(app) # Sending to the admin's email provided below

    send_to_mail(manual_review)

# views for mails
# Email configuration
smtp_server = os.environ['smtp_server']
smtp_port = os.environ['smtp_port']
sender_email = os.environ['sender_email']
sender_password = os.environ['sender_password']
recipient_email = os.environ['recipient_email']


def send_to_mail(applications):
    for app in applications:
        subject = f"Application needs Manual Review - {app.student_name}"
        message = f"Application details:\nStudent Name: {app.student_name}\nSchool Name: {app.school_name}\nAdmission Number: {app.admission_number}\nForm/Year:{app.year_of_study}\nLocation: {app.location}\nPhone Number: {app.phone_number}\nID Number: {app.id_number}"
        
        msg = MIMEMultipart()
        msg['From'] = formataddr(('Bursary system', sender_email))
        msg['To'] = recipient_email
        msg['Subject'] = subject

        msg.attach(MIMEText(message, 'plain'))

        try:
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipient_email, msg.as_string)
            server.quit()
            print('Email sent successfully!')
        except Exception as e:
            print('Error:', e)

    if __name__ == '__main__':
        process_applications()

