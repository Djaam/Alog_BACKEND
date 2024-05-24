from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Cow, SensorData
from .serializers import CowSerializer, SensorDataSerializer

@api_view(['GET', 'POST'])
def cow_list(request):
    if request.method == 'GET':
        cows = Cow.objects.all()
        serializer = CowSerializer(cows, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = CowSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def cow_detail(request, pk):
    cow = get_object_or_404(Cow, pk=pk)

    if request.method == 'GET':
        serializer = CowSerializer(cow)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = CowSerializer(cow, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        cow.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST'])
def sensor_data_list(request):
    if request.method == 'GET':
        sensor_data = SensorData.objects.all()
        serializer = SensorDataSerializer(sensor_data, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = SensorDataSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def sensor_data_detail(request, pk):
    sensor_data = get_object_or_404(SensorData, pk=pk)

    if request.method == 'GET':
        serializer = SensorDataSerializer(sensor_data)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = SensorDataSerializer(sensor_data, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        sensor_data.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
