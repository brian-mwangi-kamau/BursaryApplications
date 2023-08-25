import gspread
from oauth2client.service_account import ServiceAccountCredentials
from django.shortcuts import render
from .forms import ApplicationForm
from .models import Application
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from django.db import connections
import os
from dotenv import load_dotenv
load_dotenv()


def get_voter_info(id_number):
    with connections['external_database'].cursor() as cursor:
        cursor.execute("SELECT constituency, location FROM voter WHERE id_number = %s", [id_number])
        row = cursor.fetchone()
        if row:
            return row[0], row[1]
        return None, None
    


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

            voter_constituency, voter_location = get_voter_info(form_data['id_number'])

            if (voter_constituency == form_data['constituency'] and
                voter_location == form_data['location']):
                save_to_googlesheets(form_data)
            else:
                send_email(form_data)

            return render(request, 'success.html')
        else:
            form = ApplicationForm()
        return render(request, 'Application.html', {'form': form})


def save_to_googlesheets(data):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/spreadsheets",
             "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
    
    credentials = ServiceAccountCredentials.from_json_keyfile_name('google/credentials.json', scope)
    client = gspread.authorize(credentials)

    spreadsheet = client.open('BursaryApplications')

    worksheet = spreadsheet.get_worksheet(0)

    worksheet.append_row([
        data['student_name'],
        data['school_name'],
        data['admission_number'],
        data['year_of_study'],
        data['location']
    ])



def send_email(form_data):
    subject = 'New Application Review'
    message = f"Application details:\n\n" \
              f"Name: {form_data['student_name']}\n" \
              f"School: {form_data['school_name']}\n" \
              f"Admission Number: {form_data['admission_number']}\n" \
              f"Year of Study: {form_data['year_of_study']}\n" \
              f"Constituency: {form_data['constituency']}\n" \
              f"Location: {form_data['location']}\n" \
              f"Phone Number: {form_data['phone_number']}\n" \
              f"ID Number: {form_data['id_number']}\n"
    
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    smtp_username = os.environ('EMAIL_HOST_USER')
    smtp_password = os.environ('EMAIL_HOST_PASSWORD')
    recipient_email = os.environ('RECIPIENT_EMAIL')

    from_email = smtp_username
    to_email = recipient_email

    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(message, 'plain'))


    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.sendmail(from_email, to_email, msg.as_string())
