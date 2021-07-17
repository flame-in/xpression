from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# class Analysis(models.Model):
#     keyword = models.CharField(max_length=40)
#     result_class =  models.CharField(max_length=15)
#     sentiment_score = models.FloatField(max_length=100)

class Customer(models.Model):
	name = models.CharField(max_length=200, null=True)
	phone = models.CharField(max_length=200, null=True)
	email = models.CharField(max_length=200, null=True)
	date_created = models.DateTimeField(auto_now_add=True, null=True)
	# keyword = models.CharField(max_length=200, null=True)

	def __str__(self):
		return self.name

