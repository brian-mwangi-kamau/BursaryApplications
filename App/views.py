from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from .models import ApplicationStatus

# Create your views here.

# Homepage view 


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


# The admin profile where he/she will manage the status of applications. Whether they are open or not.
# If application is closed, by the use of a button, the admin will change the 'homepage.html' to show that there is no open appliation
def admin_profile(request):
    if request.method == 'POST':
        if 'toogle_status' in request.POST:
            # Toogling the application status between open and closed
            status_obj, created = ApplicationStatus.objects.get_or_create(pk=1)
            status_obj.is_open = not status_obj.is_open
            status_obj.save()

    status_obj, created = ApplicationStatus.objects.get_or_create(pk=1)
    is_open = status_obj.is_open

    if is_open:
        template_name = "apply.html" #This template contains a form to fill in applications (when they are open)
    else:
        template_name = "closed.html" # This template contains a message telling the user that application is closed

    return render(request, template_name)

