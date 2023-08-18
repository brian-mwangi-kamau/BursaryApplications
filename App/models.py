from django.db import models

class User(models.Model):
	username = models.CharField(max_length=100, unique=True)
	password = models.CharField(max_length=100)
	is_admin = models.BooleanField(default=False)


class BursaryApplication(models.Model):
	name = models.CharField(max_length=100)
	school = models.CharField(max_length=100)
	admission_number = models.CharField(max_length=20)
	id_number = models.CharField(max_length=8)
	constituency = models.CharField(max_length=100)
	location = models.CharField(max_length=100)
	

	class Meta:
		verbose_name_plural = 'BursaryApplications'

	def __str__(self):
		return self.name


#class DatabaseComparison(models.Model):
	# The fields to be compared against the applications

# The voter's Database Model
class ExternalDatabaseData(models.Model):
	name = models.CharField(max_length=60)
	id_number = models.IntegerField()
	constituency = models.CharField(max_length=60)
	location = models.CharField(max_length=50)


	class Meta:
		managed = False

	def __str__(self):
		return self.name