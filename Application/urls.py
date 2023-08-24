from django.urls import path
from . import views

urlpatterns = [
    path('application/', views.application_form, name='application_form'),
]
