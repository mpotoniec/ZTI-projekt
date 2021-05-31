from django.db import models
from django.conf import settings
from django.db.models.deletion import CASCADE
from django.db.models.fields.related import ForeignKey
from Services.models import Service, Station

# Create your models here.

class Reservation(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    service = ForeignKey(Service, on_delete=models.CASCADE)
    station = ForeignKey(Station, on_delete=models.CASCADE)

    reservation_from = models.DateTimeField()
    reservation_to = models.DateTimeField()
