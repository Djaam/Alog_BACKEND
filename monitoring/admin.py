from django.contrib import admin
from .models import Farmer, Cow, SensorData

admin.site.register(Farmer)
admin.site.register(Cow)
admin.site.register(SensorData)
