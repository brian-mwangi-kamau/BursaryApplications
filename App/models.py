from django.db import models



# Create your models here.
class AdminUser(models.Model):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    is_admin = models.BooleanField(default=True)


# Model for the database
class Application(models.Model):
    name_of_student = models.CharField(max_length=100)
    name_of_school = models.CharField(max_length=50)
    admission_number = models.CharField(max_length=30)
    phone_number = models.DecimalField(max_digits=15, decimal_places=0)
    gender = models.CharField(max_length=10)
    form_or_year = models.CharField(max_length=10)
    location = models.CharField(max_length=50)
    status = models.CharField(max_length=20)

    class Meta:
        unique_together = ['name_of_school', 'admission_number']



# ID number and Location
class Voter(models.Model):
    id_number = models.DecimalField(max_digits=8, decimal_places=0, unique=True)
    location = models.CharField(max_length=20)

class ApplicationStatus(models.Model):
    is_open = models.BooleanField(default=True)

    def __str__(self):
        return f"Application Status: {'Open' if self.is_open else 'Closed'}"
    

