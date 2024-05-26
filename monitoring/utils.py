from Crypto.Cipher import AES
import base64
import json
from django.utils import timezone
from datetime import timedelta
from django.db.models import Avg
from .models import SensorData, Cow


def parse_data(data_string):
    data_parts = data_string.split(',')
    data_dict = {}
    for part in data_parts:
        key, value = part.split(':')
        key = key.strip().lower()
        value = value.strip()
        if key == 'temp':
            value = float(value.replace(' C', ''))
        elif key == 'steps' or key == 'id':
            value = int(value)
        data_dict[key] = value
    data_json = json.dumps(data_dict)
    return data_json

def determine_health_status(cow):
    one_hour_ago = timezone.now() - timedelta(minutes=1)
    recent_data = SensorData.objects.filter(cow=cow, timestamp__gte=one_hour_ago)
    
    if not recent_data.exists():
        return Cow.HealthStatus.UNKNOWN

    avg_temperature = recent_data.aggregate(avg_temp=Avg('temperature'))['avg_temp']
    avg_steps = recent_data.aggregate(avg_steps=Avg('steps'))['avg_steps']
    
    if avg_temperature is None or avg_steps is None:
        return Cow.HealthStatus.UNKNOWN

    if avg_temperature < 36 or avg_temperature > 38 or avg_steps > 300 or avg_steps < 150:
        return Cow.HealthStatus.CRITICAL
    else:
        return Cow.HealthStatus.NORMAL