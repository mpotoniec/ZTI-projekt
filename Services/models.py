from django.db import models

# Create your models here.
class Service(models.Model):
    service_name = models.CharField(max_length=200)
    service_information = models.CharField(max_length=200)
    service_cost = models.CharField(max_length=200)
    service_duration = models.CharField(max_length=200)

    def __str__(self):
        return f'Nazwa usługi: {self.service_name}, koszt usługi: {self.service_cost}, czas trwania: {self.service_duration}.'

class Station(models.Model):
    station_number = models.IntegerField()
    station_description = models.CharField(max_length=200)

    def __str__(self):
        return f'Numer stanowiska: {self.station_number}, opis stanowiska: {self.station_description}.'
    