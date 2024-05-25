from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Cow, SensorData, Farmer
from .serializers import CowSerializer, SensorDataSerializer, FarmerSerializer

from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.authentication import JWTAuthentication

from Crypto.Cipher import AES
import base64
import json



AESKEY = b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0A\x0B\x0C\x0D\x0E\x0F\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1A\x1B\x1C\x1D\x1E\x1F'

def decrypt_data(data):
    encrypted_bytes = base64.b64decode(data)
    nonce = encrypted_bytes[:16]
    ciphertext = encrypted_bytes[16:]
    try:
        cipher = AES.new(AESKEY, AES.MODE_GCM, nonce=nonce)
        decrypted_data = cipher.decrypt(ciphertext)
        return decrypted_data.decode('utf-8')
    except Exception as e:
        print("Error decrypting data:", e)
        return None

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



@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
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
@permission_classes([IsAuthenticated])
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
@permission_classes([IsAuthenticated])
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
@permission_classes([IsAuthenticated])
def sensor_data_detail(request, cow_id):
    cow = get_object_or_404(Cow, id=cow_id)

    # Filter sensor data by cow_id
    sensor_data = get_object_or_404(SensorData, cow=cow)

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
        print(f"An error occurred during signup: {e}")
        return Response({"error": "An error occurred during signup"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def encryptData(request):
    try:
        encrypted_data = request.data.get('encrypted_data')
        decrypted_data = decrypt_data(encrypted_data)
        data = json.loads(parse_data(decrypted_data))
        cow_id = data.get('id')
        temperature = data.get('temp')
        steps = data.get('steps')
        cow = Cow.objects.filter(cow_id=cow_id).first()
        if not cow:
            return Response({"error": "Cow not found"}, status=status.HTTP_404_NOT_FOUND)
        sensor_data = SensorData(cow=cow, temperature=temperature, steps=steps)
        sensor_data.save()

        return Response({"message": "Data saved successfully"}, status=status.HTTP_201_CREATED)
    except Exception as e:
        print(f"An error occurred: {e}")
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
