from rest_framework import serializers
from .models import Cow, SensorData

class CowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cow
        fields = '__all__'

class SensorDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = SensorData
        fields = '__all__'

# class TreatmentSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Treatment
#         fields = '__all__'
