from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

# Register your models here.
class CustomUserAdmin(UserAdmin):
	fieldsets = (
		(None, {'fields': ('name', 'email', 'password')}),
		)
	list_display = ('name', 'email', 'is_staff')

	
'''
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ('Landing_page_template',)
'''

admin.site.register(CustomUser, UserAdmin)
#admin.site.register(SiteSettingsAdmin)