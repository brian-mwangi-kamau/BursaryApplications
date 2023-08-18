from django.urls import path
from . import views


urlpatterns = [
    path('admin/login/', views.admin_login, name="admin_login"),
    path('admin/profile/', views.admin_profile, name="admin_profile"),
]