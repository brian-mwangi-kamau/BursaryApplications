from django.contrib.auth.models import AbstractUser
#from django.contrib.auth.models import Group, Permission
from django.db import models
from django.contrib.auth import get_user_model
#from django.utils.translation import gettext as _

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



'''
class SiteSettings(models.Model):
    LANDING_PAGE_CHOICES = [
         ('NO', 'No Landing Page'), # This is the page indicating that applications are closed
         ('YES', 'Yes Landing Page'),
    ]

    landing_page_template = models.CharField(
        max_length=3, 
        choices=LANDING_PAGE_CHOICES, 
        default='NO'
    )


    groups = models.ManyToManyField(
        Group,
        verbose_name=_('groups'),
        blank=True,
        related_name='custom_users_groups'
    )

    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('user permissions'),
        blank=True,
        related_name='custom_user_permissions'
    )
    
class InboxMessage(models.Model): # The inbox feature to receive pending applications
    recipient = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    content = models.TextField()
'''
