from django.contrib import admin
from .models import Estudiante, Maquina, AccesoClase, AccesoFueraClase


@admin.register(Estudiante)
class EstudianteAdmin(admin.ModelAdmin):
    list_display = ['carnet_identidad', 'nombre', 'sexo', 'carrera', 'ano', 'edad']
    list_filter = ['sexo', 'carrera', 'ano']
    search_fields = ['carnet_identidad', 'nombre', 'carrera']
    readonly_fields = ['edad']


@admin.register(Maquina)
class MaquinaAdmin(admin.ModelAdmin):
    list_display = ['id', 'nombre_red', 'numero_ip', 'tiene_internet']
    list_filter = ['tiene_internet']
    search_fields = ['nombre_red', 'numero_ip']


@admin.register(AccesoClase)
class AccesoClaseAdmin(admin.ModelAdmin):
    list_display = ['id', 'estudiante', 'maquina', 'fecha_hora_entrada', 'fecha_hora_salida', 'asignatura', 'tipo_clase', 'profesor']
    list_filter = ['tipo_clase', 'asignatura', 'fecha_hora_entrada']
    search_fields = ['estudiante__nombre', 'estudiante__carnet_identidad', 'maquina__nombre_red', 'asignatura', 'profesor']
    date_hierarchy = 'fecha_hora_entrada'


@admin.register(AccesoFueraClase)
class AccesoFueraClaseAdmin(admin.ModelAdmin):
    list_display = ['id', 'estudiante', 'maquina', 'fecha_hora_entrada', 'fecha_hora_salida', 'motivo']
    list_filter = ['motivo', 'fecha_hora_entrada']
    search_fields = ['estudiante__nombre', 'estudiante__carnet_identidad', 'maquina__nombre_red']
    date_hierarchy = 'fecha_hora_entrada'
