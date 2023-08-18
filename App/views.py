from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
#from django.shortcuts import get_object_or_404
from django.http import HttpResponse



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


# Admin inbox


