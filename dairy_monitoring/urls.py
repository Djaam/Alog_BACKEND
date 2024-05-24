from django.contrib import admin
from django.urls import path
from monitoring import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/cows/', views.cow_list, name='cow_list'),
    path('api/cows/<int:pk>/', views.cow_detail, name='cow_detail'),
    path('api/sensor-data/', views.sensor_data_list, name='sensor_data_list'),
    path('api/sensor-data/<int:pk>/', views.sensor_data_detail, name='sensor_data_detail'),
    
]
