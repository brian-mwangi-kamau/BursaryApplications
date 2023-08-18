
from django import forms
from .models import BursaryApplication

class BursaryApplicationForm(forms.ModelForm):
    class Meta:
        model = BursaryApplication
        fields = ['name', 'school', 'admission_number', 'id_number', 'constituency', 'location']


