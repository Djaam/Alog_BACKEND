from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Cow, SensorData, Farmer
from .serializers import CowSerializer, SensorDataSerializer, FarmerSerializer

from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.authentication import JWTAuthentication

import json
from .utils import parse_data, determine_health_status



@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def cow_list(request):
    if request.method == 'GET':
        cows = Cow.objects.filter(farmer=request.user)
        serializer = CowSerializer(cows, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = CowSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def cow_detail(request, pk):
    try:
        cow = get_object_or_404(Cow, pk=pk)
    except Cow.DoesNotExist:
        return Response({"error": "Cow not found"}, status=status.HTTP_404_NOT_FOUND)

    if cow.farmer != request.user:
        return Response({"error": "You do not have permission to perform this action"}, status=status.HTTP_403_FORBIDDEN)

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
@permission_classes([IsAuthenticated])
def sensor_data_list(request):
    if request.method == 'GET':
        sensor_data = SensorData.objects.filter(cow__farmer=request.user)
        serializer = SensorDataSerializer(sensor_data, many=True)
        return Response(serializer.data)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def sensor_data_detail(request, cow_id):
    cow = get_object_or_404(Cow, cow_id=cow_id)

    if cow.farmer != request.user:
        return Response({"error": "You do not have permission to access this data"}, status=status.HTTP_403_FORBIDDEN)

    sensor_data = SensorData.objects.filter(cow=cow).order_by('-timestamp')[:100]

    if request.method == 'GET':
        temperature_data = sensor_data.values('timestamp', 'temperature')
        steps_data = sensor_data.values('timestamp', 'steps')

        response_data = {
            'temperature': list(temperature_data),
            'steps': list(steps_data)
        }

        return Response(response_data)


@api_view(['POST'])
def signup(request):
    try:
        serializer = FarmerSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error": "An error occurred during signup"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def recieveData(request):
    try:
        data = request.data.get('data')
        data = json.loads(parse_data(data))
        cow_id = data.get('id')
        temperature = data.get('temp')
        steps = data.get('steps')
        cow = Cow.objects.filter(cow_id=cow_id).first()
        if not cow:
            return Response({"error": "Cow not found"}, status=status.HTTP_404_NOT_FOUND)
        sensor_data = SensorData(cow=cow, temperature=temperature, steps=steps)
        sensor_data.save()

        health_status = determine_health_status(cow)
        cow.health_status = health_status
        print(f"Health status for cow {cow_id}: {health_status}")
        cow.save()

        return Response({"message": "Data saved successfully"}, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({"error": "An error occurred during data processing"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@api_view(['POST'])
def login(request):
    try:
        email = request.data.get('email')
        password = request.data.get('password')
        
        user = Farmer.objects.get(email=email)
        
        if not user.check_password(password):
            return Response({"error": "Invalid email or password"}, status=status.HTTP_401_UNAUTHORIZED)
        
        access = AccessToken.for_user(user)
        
        return Response({
            'token': str(access),
            'user': {
                'id': user.id,
                'fullname': user.fullname,
                'address': user.address,
                'farm_name': user.farm_name,
                'date_joined': user.date_joined,
                'email': user.email
            }
        })
        
    except Farmer.DoesNotExist:
        return Response({"error": "Invalid email or password"}, status=status.HTTP_401_UNAUTHORIZED)
