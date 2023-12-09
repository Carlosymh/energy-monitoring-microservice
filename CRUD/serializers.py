from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import Dispositivo, TiposDispositivo, StatusDispositivo, Lecturas, Mantenimientos

class DispositivoSerializer(ModelSerializer):
    class Meta:
        model=Dispositivo
        fields='__all__'
        read_only_fields = ('id',)

class TiposDispositivoSerializer(ModelSerializer):
    class Meta:
        model=TiposDispositivo
        fields='__all__'
        read_only_fields = ('id',)

class StatusDispositivoSerializer(ModelSerializer):
    class Meta:
        model=StatusDispositivo
        fields='__all__'
        read_only_fields = ('id',)
        
class LecturasSerializer(ModelSerializer):
    class Meta:
        model=Lecturas
        fields='__all__'
        read_only_fields = ('id',)
        
class MantenimientosSerializer(ModelSerializer):
    class Meta:
        model=Mantenimientos
        fields='__all__'
        read_only_fields = ('id',)

class EnergiaTotalSerializer(serializers.Serializer):
    iddispositivo = serializers.IntegerField()
    energia_total = serializers.FloatField()