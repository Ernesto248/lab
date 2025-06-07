from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from django.db.models import Q, Count
from django.utils.dateparse import parse_datetime
from datetime import datetime, timedelta
from .models import Estudiante, Maquina, AccesoClase, AccesoFueraClase
from .serializers import EstudianteSerializer, MaquinaSerializer, AccesoClaseSerializer, AccesoFueraClaseSerializer


class EstudianteViewSet(viewsets.ModelViewSet):
    queryset = Estudiante.objects.all()
    serializer_class = EstudianteSerializer


class MaquinaViewSet(viewsets.ModelViewSet):
    queryset = Maquina.objects.all()
    serializer_class = MaquinaSerializer


class AccesoClaseViewSet(viewsets.ModelViewSet):
    queryset = AccesoClase.objects.all()
    serializer_class = AccesoClaseSerializer
    
    @action(detail=False, methods=['get'])
    def por_maquina_asignatura(self, request):
        """Endpoint para listar estudiantes por máquina y asignatura"""
        maquina_id = request.query_params.get('maquina_id')
        asignatura = request.query_params.get('asignatura')
        
        if not maquina_id or not asignatura:
            return Response(
                {'error': 'Se requieren los parámetros maquina_id y asignatura'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        accesos = AccesoClase.objects.filter(
            maquina_id=maquina_id,
            asignatura=asignatura
        )
        
        serializer = self.get_serializer(accesos, many=True)
        return Response(serializer.data)


class AccesoFueraClaseViewSet(viewsets.ModelViewSet):
    queryset = AccesoFueraClase.objects.all()
    serializer_class = AccesoFueraClaseSerializer


@api_view(['POST'])
def calcular_aee(request):
    """Endpoint para calcular el AEE (Aprovechamiento Estimado de Estancia)"""
    carnet_identidad = request.data.get('carnet_identidad')
    fecha_hora_entrada = request.data.get('fecha_hora_entrada')
    
    if not carnet_identidad or not fecha_hora_entrada:
        return Response(
            {'error': 'Se requieren carnet_identidad y fecha_hora_entrada'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        fecha_entrada = parse_datetime(fecha_hora_entrada)
        if not fecha_entrada:
            return Response(
                {'error': 'Formato de fecha inválido'},
                status=status.HTTP_400_BAD_REQUEST
            )
    except:
        return Response(
            {'error': 'Formato de fecha inválido'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Buscar en AccesoClase
    acceso_clase = AccesoClase.objects.filter(
        estudiante__carnet_identidad=carnet_identidad,
        fecha_hora_entrada=fecha_entrada
    ).first()
    
    # Buscar en AccesoFueraClase si no se encontró en AccesoClase
    acceso_fuera = None
    if not acceso_clase:
        acceso_fuera = AccesoFueraClase.objects.filter(
            estudiante__carnet_identidad=carnet_identidad,
            fecha_hora_entrada=fecha_entrada
        ).first()
    
    acceso = acceso_clase or acceso_fuera
    
    if not acceso or not acceso.fecha_hora_salida:
        return Response(
            {'error': 'No se encontró el acceso o no tiene fecha de salida'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    # Calcular duración en minutos
    duracion = acceso.fecha_hora_salida - acceso.fecha_hora_entrada
    duracion_minutos = duracion.total_seconds() / 60
    
    # Aplicar porcentaje según tipo
    porcentaje_aprovechamiento = 1.0  # 100% por defecto
    
    if acceso_clase:
        # Porcentajes para tipos de clase
        porcentajes_clase = {
            'LAB': 0.85,  # 85% para laboratorio
            'SEM': 0.90,  # 90% para seminario
            'EP': 0.95,   # 95% para evaluación parcial
            'EF': 0.98,   # 98% para evaluación final
        }
        porcentaje_aprovechamiento = porcentajes_clase.get(acceso.tipo_clase, 1.0)
    else:
        # Porcentajes para motivos fuera de clase
        porcentajes_fuera = {
            'PROY': 0.80,  # 80% para proyecto
            'TRAB': 0.75,  # 75% para trabajo extra clase
            'OTRO': 0.60,  # 60% para otro
        }
        porcentaje_aprovechamiento = porcentajes_fuera.get(acceso.motivo, 1.0)
    
    aprovechamiento_minutos = duracion_minutos * porcentaje_aprovechamiento
    
    return Response({
        'aprovechamiento_minutos': round(aprovechamiento_minutos, 2)
    })


@api_view(['GET'])
def estudiante_por_maquina_tiempo(request):
    """Endpoint para encontrar estudiante por máquina y tiempo"""
    maquina_id = request.query_params.get('maquina_id')
    fecha_hora = request.query_params.get('fecha_hora')
    
    if not maquina_id or not fecha_hora:
        return Response(
            {'error': 'Se requieren los parámetros maquina_id y fecha_hora'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        fecha_consulta = parse_datetime(fecha_hora)
        if not fecha_consulta:
            return Response(
                {'error': 'Formato de fecha inválido'},
                status=status.HTTP_400_BAD_REQUEST
            )
    except:
        return Response(
            {'error': 'Formato de fecha inválido'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Buscar en AccesoClase
    acceso_clase = AccesoClase.objects.filter(
        maquina_id=maquina_id,
        fecha_hora_entrada__lte=fecha_consulta,
        fecha_hora_salida__gte=fecha_consulta
    ).first()
    
    # Buscar en AccesoFueraClase si no se encontró
    acceso_fuera = None
    if not acceso_clase:
        acceso_fuera = AccesoFueraClase.objects.filter(
            maquina_id=maquina_id,
            fecha_hora_entrada__lte=fecha_consulta,
            fecha_hora_salida__gte=fecha_consulta
        ).first()
    
    acceso = acceso_clase or acceso_fuera
    
    if not acceso:
        return Response(
            {'error': 'No se encontró ningún estudiante en esa máquina en el tiempo especificado'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    serializer = EstudianteSerializer(acceso.estudiante)
    return Response(serializer.data)


@api_view(['GET'])
def uso_por_carrera(request):
    """Endpoint para determinar el año de una carrera que más usa el laboratorio"""
    carrera = request.query_params.get('carrera')
    
    if not carrera:
        return Response(
            {'error': 'Se requiere el parámetro carrera'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Contar accesos por año en la carrera especificada
    uso_por_ano = AccesoClase.objects.filter(
        estudiante__carrera=carrera
    ).values('estudiante__ano').annotate(
        total_accesos=Count('id')
    ).order_by('-total_accesos')
    
    if not uso_por_ano:
        return Response(
            {'error': f'No se encontraron accesos para la carrera {carrera}'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    ano_mas_uso = uso_por_ano[0]['estudiante__ano']
    
    return Response({
        'carrera': carrera,
        'ano_mas_uso': ano_mas_uso
    })


@api_view(['GET'])
def uso_semanal(request):
    """Endpoint para listado de estudiantes en una semana, ordenado por edad"""
    fecha_inicio_str = request.query_params.get('fecha_inicio')
    
    if not fecha_inicio_str:
        return Response(
            {'error': 'Se requiere el parámetro fecha_inicio'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        fecha_inicio = datetime.strptime(fecha_inicio_str, '%Y-%m-%d').date()
        fecha_fin = fecha_inicio + timedelta(days=7)
    except ValueError:
        return Response(
            {'error': 'Formato de fecha inválido. Use YYYY-MM-DD'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Obtener estudiantes únicos que tuvieron accesos en la semana
    estudiantes_clase = AccesoClase.objects.filter(
        fecha_hora_entrada__date__gte=fecha_inicio,
        fecha_hora_entrada__date__lt=fecha_fin
    ).values_list('estudiante__carnet_identidad', flat=True).distinct()
    
    estudiantes_fuera = AccesoFueraClase.objects.filter(
        fecha_hora_entrada__date__gte=fecha_inicio,
        fecha_hora_entrada__date__lt=fecha_fin
    ).values_list('estudiante__carnet_identidad', flat=True).distinct()
    
    # Combinar y obtener únicos
    carnets_unicos = set(list(estudiantes_clase) + list(estudiantes_fuera))
    
    # Obtener objetos estudiante
    estudiantes = Estudiante.objects.filter(carnet_identidad__in=carnets_unicos)
    
    # Ordenar por edad (calculada)
    estudiantes_ordenados = sorted(estudiantes, key=lambda e: e.edad or 0)
    
    serializer = EstudianteSerializer(estudiantes_ordenados, many=True)
    return Response(serializer.data)
