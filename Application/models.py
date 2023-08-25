from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    name = models.CharField(max_length=10)
    email = models.EmailField(unique=True)

    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name='customuser_set', 
        related_query_name='user',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name='customuser_set',
        related_query_name='user',
    )

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

