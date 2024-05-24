from django.contrib import admin

from .models import Cow, SensorData

# Register your models here.
admin.site.register(Cow)
admin.site.register(SensorData)
