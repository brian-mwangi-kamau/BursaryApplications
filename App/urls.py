from django.urls import path
from . import views

urlpatterns = [
path('apply/', views.apply_for_bursary, name='apply_for_bursary'),
]