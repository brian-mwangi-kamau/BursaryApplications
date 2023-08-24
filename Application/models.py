from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth import get_user_model



class CustomUser(AbstractUser):
    name = models.CharField(max_length=10)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if self.password and not self.password.startswith('pbkdf2_sha256$'):
            self.set_password(self.password)
        super(CustomUser, self).save(*args, **kwargs)


class Application(models.Model):
    student_name = models.CharField(max_length=255)
    school_name = models.CharField(max_length=255)
    admission_number = models.CharField(max_length=20)
    year_of_study = models.CharField(max_length=50)
    constituency = models.CharField(max_length=15)
    location = models.CharField(max_length=15)
    phone_number = models.CharField(max_length=10)
    id_number = models.CharField(max_length=8)
    submission_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.student_name


# Model for comparison
class VoterDatabase(models.Model):
    id_number = models.CharField(max_length=8)
    constituency = models.CharField(max_length=15)
    location = models.CharField(max_length=15)
    
    def __str__(self):
        return self.id_number
    

