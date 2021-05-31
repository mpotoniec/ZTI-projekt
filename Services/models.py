from django.db import models

# Create your models here.
class Service(models.Model):
    service_name = models.CharField(max_length=200)
    service_information = models.CharField(max_length=200)
    service_cost = models.CharField(max_length=200)
    service_duration = models.CharField(max_length=200)

class Station(models.Model):
    station_number = models.IntegerField()
    station_description = models.CharField(max_length=200)
    