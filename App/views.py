from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
#from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from .models import ApplicationStatus, Application
from .models import Voter
from .forms import ApplicationForm
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from django.contrib.auth.decorators import login_required
from django.db import connections
# Create your views here.
# Homepage view 
def homepage(request):
    # Toogling the application status between open and closed
    # The admin profile where he/she will manage the status of applications. Whether they are open or not.
    # If application is closed, by the use of a button, the admin will change the 'homepage.html' to show that there is no open appliation
    status_obj, created = ApplicationStatus.objects.get_or_create(pk=1)
    is_open = status_obj.is_open

    template_name = "apply.html" if is_open else "closed.html"
    return render(request, template_name)



#Admin Login view
def admin_login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)

        if user is not None and user.is_admin:
            login(request, user)
            return redirect('admin_profile')
        
        else:
            response = HttpResponse('Access barred!')
            return response
        
    return render(request, 'admin_login.html')


# Admin management profile
# This is where the admin will control features like toggling home pages
def admin_profile(request):
    return render(request, "admin_profile.html")

            

# Application submission view
def apply(request):
    if request.method == 'POST':
        form = ApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            location = application.location
            id_number = application.id_number

            with connections['external_db'].cursor() as cursor:
                cursor.execute("SELECT id_number, location FROM voter WHERE id_number = %s AND location = %s", [id_number, location])
                row = cursor.fetchone()

                if row:
                    application.status = 'Accepted'
                else:
                    application.status = 'Pending'

            try:
                voter = Voter.objects.get(id_number=id_number, location=location)
                application.status = 'Accepted'
            except Voter.DoesNotExist:
                application.status = 'Pending'

            # Logic to push to google spreadsheets
            if application.status == 'Accepted':
                creds = Credentials.from_authorized_user_file('path_to_the_credentials')
                service = build('sheets', 'v4', credentials=creds)

                spreadsheet_id = 'the_spreadsheet_id'
                range_name = 'Sheet1!A2:F2'

                values = [
                    [application.name_of_student, application.name_of_school, application.admission_number, application.gender, application.form_or_year, application.location]
                ]

                request = service.spreadsheets().values().append(spreadsheetId=spreadsheet_id, range=range_name, valueInputOption='RAW', insertDataOption='INSERT_ROWS', body={'values': values})
                response = request.execute()

            application.save()
            return redirect('application_submitted')
        else:
            form = ApplicationForm()

        context = {'form': form}
        return render(request, 'application_form.html', context)

    
# Admin inbox
@login_required
def admin_inbox(request):
    pending_applications = Application.objects.filter(status='Pending')
    context = {'pending_applications': pending_applications}
    return render(request, 'admin_inbox.html', context)

