from rest_framework.response import Response
from rest_framework.decorators import api_view, schema
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from django.http import Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Sum
from .models import Dispositivo, TiposDispositivo, StatusDispositivo, Lecturas, Mantenimientos
from .serializers import DispositivoSerializer, TiposDispositivoSerializer, StatusDispositivoSerializer, LecturasSerializer, MantenimientosSerializer, EnergiaTotalSerializer

#Get All Divices
@api_view(['GET'])
def getDevices(request):
    dispositivos = Dispositivo.objects.all()
    paginator = Paginator(dispositivos, 30)  
    page = request.GET.get('page')
    try:
        dispositivos = paginator.page(page)
    except PageNotAnInteger:
        dispositivos = paginator.page(1)
    except EmptyPage:
        dispositivos = paginator.page(paginator.num_pages)

    serializer = DispositivoSerializer(dispositivos, many=True)
    return Response(serializer.data)

#Get One  Divice
@api_view(['GET'])
def getDevice(request,pk):
    dispositivo = Dispositivo.objects.get(id=pk)
    serializer = DispositivoSerializer(dispositivo, many=False)
    return Response(serializer.data)

#Get One  Divice
@api_view(['GET'])
def getDevicesForType(request,tipodispositivoId):
    dispositivo = Dispositivo.objects.filter(tipodispositivoId=tipodispositivoId)
    serializer = DispositivoSerializer(dispositivo, many=True)
    return Response(serializer.data)

#Create Divice
@swagger_auto_schema(
    method='post',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'nombre_equipo': {'type': 'string', 'description': 'Nombre del Dispositivo.'},
            'tipodispositivoId': {'type': 'integer', 'description': 'ID del Tipo de Dispositivo.'},
            'potencia_actual': {'type': 'integer', 'description': 'Potenci actual (KW), solo digitos.'},
            'statusDispositivoId': {'type': 'integer', 'description': 'Id Status Dispositivo.'},
        },
        required=['nombre_equipo', 'tipodispositivoId', 'potencia_actual', 'statusDispositivoId']
    ),
    responses={200: 'Respuesta exitosa'}
)
@api_view(['POST'])
def createDevice(request):
    data=request.data
    
    if not TiposDispositivo.objects.filter(id=data['tipodispositivoId']).exists():
        return Response("El TipoDispositivoId no existe.",status=status.HTTP_400_BAD_REQUEST)

    if not StatusDispositivo.objects.filter(id=data['statusDispositivoId']).exists():
        return Response("El StatusDispositivoId no existe.",status=status.HTTP_400_BAD_REQUEST)
        
    dispositivos = Dispositivo.objects.create(
        nombre_equipo=data['nombre_equipo'],
        tipodispositivoId=TiposDispositivo.objects.get(id=data['tipodispositivoId']),
        potencia_actual=data['potencia_actual'],
        statusDispositivoId=StatusDispositivo.objects.get(id=data['statusDispositivoId'])
    )
    serializer=DispositivoSerializer(dispositivos, many=False)
    return Response(serializer.data,status=status.HTTP_201_CREATED)


#Create Divice
@swagger_auto_schema(
    method='put',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'nombre_equipo': {'type': 'string', 'description': 'Nombre del Dispositivo.'},
            'tipodispositivoId': {'type': 'integer', 'description': 'ID del Tipo de Dispositivo.'},
            'potencia_actual': {'type': 'integer', 'description': 'Potenci actual (KW), solo digitos.'},
            'statusDispositivoId': {'type': 'integer', 'description': 'Id Status Dispositivo.'},
        }
    ),
    responses={200: 'Respuesta exitosa'}
)
@api_view(['PUT'])
def updateDevice(request,pk):
    data=request.data
    print(request,request.data)
    dispositivos =  Dispositivo.objects.get(id=pk)
    if data.get('tipodispositivoId'): 
        if not TiposDispositivo.objects.filter(id=data['tipodispositivoId']).exists():
            return Response("El TipoDispositivoId no existe.",status=status.HTTP_400_BAD_REQUEST)
        dispositivos.tipodispositivoId=TiposDispositivo.objects.get(id=data['tipodispositivoId'])
    if data.get('statusDispositivoId'): 
        if not StatusDispositivo.objects.filter(id=data['statusDispositivoId']).exists():
            return Response("El StatusDispositivoId no existe.",status=status.HTTP_400_BAD_REQUEST)
        dispositivos.statusDispositivoId=StatusDispositivo.objects.get(id=data['statusDispositivoId'])
        
    if data.get('potencia_actual'): dispositivos['potencia_actual']=data['potencia_actual']
    if data.get('nombre_equipo'): dispositivos['nombre_equipo']=data['nombre_equipo']
    

    dispositivos.save()
    print(dispositivos)
    serializer=DispositivoSerializer(dispositivos)
    return Response(serializer.data)


#Get All Readings
@api_view(['GET'])
def getReadings(request):
    lecturas = Lecturas.objects.all()
    paginator = Paginator(lecturas, 30)
    page = request.GET.get('page')
    try:
        lecturas = paginator.page(page)
    except PageNotAnInteger:
        lecturas = paginator.page(1)
    except EmptyPage:
        lecturas = paginator.page(paginator.num_pages)

    serializer = LecturasSerializer(lecturas, many=True)
    return Response(serializer.data)


#Get One  Reading
@api_view(['GET'])
def getReading(request,pk):
    lectura = Lecturas.objects.get(id=pk)
    serializer = LecturasSerializer(lectura, many=False)
    return Response(serializer.data)

#Get One  Reading
@api_view(['GET'])
def getReadingsForType(request,tipodispositivoId):
    lecturas = Lecturas.objects.filter(tipodispositivoId=tipodispositivoId)
    serializer = LecturasSerializer(lecturas, many=True)
    return Response(serializer.data)


#Create Reading
@swagger_auto_schema(
    method='post',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'iddispositivo': {'type': 'integer', 'description': 'ID del Dispositivo.'},
            'idtipodispositivo': {'type': 'integer', 'description': 'ID del Tipo de Dispositivo.'},
            'potenciaActual': {'type': 'float', 'description': 'Potenci actual (KW), solo digitos.'},
        },
        required=['iddispositivo', 'idtipodispositivo', 'potenciaActual']
    ),
    responses={200: 'Respuesta exitosa'}
)
@api_view(['POST'])
def createReading(request):
    data=request.data
    lecttura = Lecturas.objects.create(
        iddispositivo=Dispositivo.objects.get(id=data['iddispositivo']),
        idtipodispositivo=TiposDispositivo.objects.get(id=data['idtipodispositivo']),
        potenciaActual=data['potenciaActual']
    )
    
    serializer=LecturasSerializer(lecttura, many=False)
    return Response(serializer.data,status=status.HTTP_201_CREATED)

#Get Full Energy
@api_view(['GET'])
def getFullEnergy(request):
    energia_total_por_dispositivo =  Lecturas.objects.values('iddispositivo').annotate(energia_total=Sum('potenciaActual'))
    print(energia_total_por_dispositivo)
    paginator = Paginator(energia_total_por_dispositivo, 30)
    page = request.GET.get('page')
    try:
        energia_total_por_dispositivo = paginator.page(page)
    except PageNotAnInteger:
        energia_total_por_dispositivo = paginator.page(1)
    except EmptyPage:
        energia_total_por_dispositivo = paginator.page(paginator.num_pages)
    

    serializer = EnergiaTotalSerializer(energia_total_por_dispositivo, many=True)
    return Response(serializer.data)

#Get Maintenance Record
@api_view(['GET'])
def getMaintenanceRecord(request):
    mantenimientos = Mantenimientos.objects.all()
    paginator = Paginator(mantenimientos, 30)
    page = request.GET.get('page')
    try:
        mantenimientos = paginator.page(page)
    except PageNotAnInteger:
        mantenimientos = paginator.page(1)
    except EmptyPage:
        mantenimientos = paginator.page(paginator.num_pages)

    serializer = MantenimientosSerializer(mantenimientos, many=True)
    return Response(serializer.data)

# Get Status Dispositivo
@api_view(['GET'])
def getStatusDispositivo(request):
    statusDispositivo = StatusDispositivo.objects.all()
    serializer = StatusDispositivoSerializer(statusDispositivo, many=True)
    return Response(serializer.data)


# Get Tipos Dispositivo
@api_view(['GET'])
def getTiposDispositivo(request):
    tiposDispositivo = TiposDispositivo.objects.all()
    serializer = TiposDispositivoSerializer(tiposDispositivo, many=True)
    return Response(serializer.data)