from django.db import models
from django.contrib.auth.models import User

class Cow(models.Model):
    farmer = models.ForeignKey(User, on_delete=models.CASCADE)
    id = models.IntegerField(primary_key=True)
    health_status = models.CharField(max_length=100)

class SensorData(models.Model):
    cow = models.ForeignKey(Cow, on_delete=models.CASCADE)
    temperature = models.FloatField()
    steps = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)

# class Treatment(models.Model):
#     cow = models.ForeignKey(Cow, on_delete=models.CASCADE)
#     veterinarian = models.ForeignKey(User, on_delete=models.CASCADE)
#     description = models.TextField()
#     date = models.DateTimeField(auto_now_add=True)
