from django.contrib import admin
from django.urls import path
from monitoring import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/signup/', views.signup, name='signup'),
    path('api/login/', views.login, name='login'),
    path('api/cows/', views.cow_list, name='cow_list'),
    path('api/cows/<int:pk>/', views.cow_detail, name='cow_detail'),
    path('api/sensor-data/', views.sensor_data_list, name='sensor_data_list'),
    path('api/encrypted-data/', views.encryptData, name='encryptData'),
    path('sensor-data/<int:cow_id>/', views.sensor_data_detail, name='sensor_data_detail'),
    
]
