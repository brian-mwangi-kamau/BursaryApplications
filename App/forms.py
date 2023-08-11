from django import forms
from .models import Applications

class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Applications
        fields = '__all__'

