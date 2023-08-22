from django.shortcuts import render, redirect
#from .models import SiteSettings
from .forms import ApplicationForm
from . models import Application
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


'''
def landing_page(request):
    settings = SiteSettings.objects.first()

    if settings.landing_page_template == 'NO':
        template_name = 'landing_no.html'
    else:
        template_name = 'landing_yes.html'

    return render(request, template_name)
'''
    