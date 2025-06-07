from rest_framework import serializers
from .models import Estudiante, Maquina, AccesoClase, AccesoFueraClase


class EstudianteSerializer(serializers.ModelSerializer):
    edad = serializers.ReadOnlyField()
    
    class Meta:
        model = Estudiante
        fields = ['carnet_identidad', 'nombre', 'sexo', 'carrera', 'ano', 'edad']


class MaquinaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Maquina
        fields = '__all__'


class AccesoClaseSerializer(serializers.ModelSerializer):
    estudiante_datos = EstudianteSerializer(source='estudiante', read_only=True)
    maquina_datos = MaquinaSerializer(source='maquina', read_only=True)
    
    class Meta:
        model = AccesoClase
        fields = '__all__'


class AccesoFueraClaseSerializer(serializers.ModelSerializer):
    estudiante_datos = EstudianteSerializer(source='estudiante', read_only=True)
    maquina_datos = MaquinaSerializer(source='maquina', read_only=True)
    
    class Meta:
        model = AccesoFueraClase
        fields = '__all__'
