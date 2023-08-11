from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
#from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from .models import ApplicationStatus, Applications
from .forms import ApplicationForm

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
            # Compare the provided ID number to the one on the database from IEBC

            application.save()
            return redirect('application_submitted') #Done!
        
        else:
            form = ApplicationForm # Back to square one

        context = {'form': form}
        return render(request, 'application_form.html', context)
    
