from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
#from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from .models import ExternalDatabaseData
#import gspread # google spreadsheets
#from oauth2client.service_account import ServiceAccountCredentials
from .models import BursaryApplication
from .forms import BursaryApplicationForm

# View for applying forms
def apply_for_bursary(request):
    if request.method == 'POST':
        form = BursaryApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False) # Not yet time to save to the database
            # The logic for comparison of the constituency, location and Id_number

            application.save() # Saving to the database
            return redirect('application_success')

        else:
            form = BursaryApplicationForm()

        return render(request, 'application_form.html', {'form': form})




# View for filling valid applications to google spreadsheets automatically follow

#def view_external_data(request):
 #   external_data = ExternalDatabaseData.objects.using('Applications App'),all()



