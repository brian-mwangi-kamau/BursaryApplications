from django import forms
from .models import Application


class ApplicationForm(forms.Form):
    student_name = forms.CharField(max_length=255, label="Name of Student")
    school_name = forms.CharField(max_length=255, label="Name of School")
    admission_number = forms.CharField(max_length=30, label="Admission Number")
    year_of_study = forms.CharField(max_length=50, label="Form or Year of Study")
    constituency = forms.CharField(max_length=15)
    location = forms.CharField(max_length=15)
    phone_number = forms.CharField(max_length=10, validators=[...])
    id_number = forms.CharField(max_length=8)

    class Meta:
        model = Application
        fields = '__all__'