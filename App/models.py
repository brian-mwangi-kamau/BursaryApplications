from django.db import models



# Create your models here.
class AdminUser(models.Model):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    is_admin = models.BooleanField(default=True)


# Model for the database
class Applications(models.Model):
    Name_of_student = models.CharField(max_length=100)
    Name_of_school = models.CharField(max_length=50)
    Admission_number = models.CharField(max_length=30)
    ID_card_number = models.DecimalField(max_digits=8, decimal_places=0)
    Phone_number = models.DecimalField(max_digits=15, decimal_places=0)
    Gender = models.CharField(max_length=10)
    Form_or_Year = models.CharField(max_length=10)
    Location = models.CharField(max_length=20)


class ApplicationStatus(models.Model):
    is_open = models.BooleanField(default=True)

    def __str__(self):
        return f"Application Status: {'Open' if self.is_open else 'Closed'}"
    
