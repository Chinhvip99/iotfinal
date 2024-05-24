from django.db import models
from django.utils import timezone

class Iot(models.Model):
    name = models.CharField(max_length=100)
    value = models.CharField(max_length=255)
    time_created = models.DateTimeField()

class TCL(models.Model):
    temp= models.CharField(max_length=225)
    light= models.CharField(max_length=225)
    hum= models.CharField(max_length=225)
    time_created = models.DateTimeField()

    
