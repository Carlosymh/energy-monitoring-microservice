from django.contrib import admin
from .models import Dispositivo, TiposDispositivo, StatusDispositivo, Lecturas, Mantenimientos

admin.site.register(Dispositivo)
admin.site.register(TiposDispositivo)
admin.site.register(StatusDispositivo)
admin.site.register(Lecturas)
admin.site.register(Mantenimientos)