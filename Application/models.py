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
