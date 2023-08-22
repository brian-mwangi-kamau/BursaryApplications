from django.urls import path
from django.contrib.auth import views as auth_views
from Application import views

urlpatterns = [
    #path('home/', views.landing_page, name='landing_page'),
    path('admin/password_change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('application/', views.application_form, name='Application form'),
    path('application/success/', views.success, name='application success')
]

