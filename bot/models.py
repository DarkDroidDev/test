from django.db import models

# Create your models here.


class User(models.Model):
	id = models.BigIntegerField(primary_key=True, unique=True)
	referrees = models.IntegerField(default=0)
	overflow = models.IntegerField(default=0)
	link = models.URLField(max_length=100, blank=True, null=True)
	referral_link = models.URLField(max_length=100, blank=True, null=True)
	name = models.CharField(max_length=100)
	status = models.BooleanField(default=False)
	note = models.CharField(max_length=300, default='')
		
	
	def __str__(self):
		return self.name
	
	
class Translation(models.Model):
	lookup = models.CharField(max_length=15)
	translated_text = models.CharField(max_length=250)
	lang = models.CharField(max_length=5)
	
	def __str__(self):
		return self.lookup
