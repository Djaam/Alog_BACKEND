from rest_framework import serializers
from .models import Cow, SensorData, Farmer


class FarmerSerializer(serializers.ModelSerializer) : 
    class Meta : 
        model = Farmer
        fields = ['id','fullname','address','farm_name','date_joined','email','password']

    def create(self, validated_data):
        user = Farmer.objects.create_user(**validated_data)
        return user

class CowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cow
        fields = ['farmer', 'cow_id', 'health_status']

class SensorDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = SensorData
        fields = "__all__"
