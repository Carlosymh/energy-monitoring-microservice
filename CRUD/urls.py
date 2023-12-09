from django.urls import path
from . import views

urlpatterns = [
    path('getDevices/',views.getDevices),
    path('getDevice/<int:pk>',views.getDevice),
    path('getDevicesForType/<int:tipodispositivoId>',views.getDevicesForType),
    path('createDevice/',views.createDevice),
    path('updateDevice/<int:pk>',views.updateDevice),
    path('getReadings/',views.getReadings),
    path('getReading/<int:pk>',views.getReading),
    path('getReadingsForType/<int:tipodispositivoId>',views.getReadingsForType),
    path('createReading/',views.createReading),
    path('getFullEnergy/',views.getFullEnergy),
    path('getMaintenanceRecord/',views.getMaintenanceRecord),
    path('getStatusDispositivo/',views.getStatusDispositivo),
    path('getTiposDispositivo/',views.getTiposDispositivo),

]
