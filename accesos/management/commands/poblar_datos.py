from django.core.management.base import BaseCommand
from django.utils import timezone
from accesos.models import Estudiante, Maquina, AccesoClase, AccesoFueraClase
from datetime import datetime, timedelta
import random


class Command(BaseCommand):
    help = 'Poblar la base de datos con datos de ejemplo para el sistema de control de accesos'

    def handle(self, *args, **options):
        self.stdout.write('Iniciando población de datos...')
        
        # Limpiar datos existentes
        AccesoFueraClase.objects.all().delete()
        AccesoClase.objects.all().delete()
        Maquina.objects.all().delete()
        Estudiante.objects.all().delete()
        
        # Crear estudiantes
        estudiantes_data = [
            {'carnet': '95032112345', 'nombre': 'Ana García López', 'sexo': 'F', 'carrera': 'Informatica', 'ano': 3},
            {'carnet': '96051598765', 'nombre': 'Carlos Rodríguez Pérez', 'sexo': 'M', 'carrera': 'Informatica', 'ano': 4},
            {'carnet': '97081223456', 'nombre': 'María Fernández Castro', 'sexo': 'F', 'carrera': 'Sistemas', 'ano': 2},
            {'carnet': '98092334567', 'nombre': 'José Luis Martín González', 'sexo': 'M', 'carrera': 'Informatica', 'ano': 3},
            {'carnet': '99120145678', 'nombre': 'Laura Sánchez Rivera', 'sexo': 'F', 'carrera': 'Sistemas', 'ano': 1},
            {'carnet': '00030256789', 'nombre': 'Pedro Jiménez Torres', 'sexo': 'M', 'carrera': 'Informatica', 'ano': 5},
            {'carnet': '01071167890', 'nombre': 'Carmen Díaz Morales', 'sexo': 'F', 'carrera': 'Sistemas', 'ano': 2},
            {'carnet': '02092278901', 'nombre': 'Miguel Ruiz Herrera', 'sexo': 'M', 'carrera': 'Informatica', 'ano': 4},
            {'carnet': '03041389012', 'nombre': 'Isabel López Vega', 'sexo': 'F', 'carrera': 'Sistemas', 'ano': 3},
            {'carnet': '04062490123', 'nombre': 'Antonio García Ramos', 'sexo': 'M', 'carrera': 'Informatica', 'ano': 1},
        ]
        
        estudiantes = []
        for data in estudiantes_data:
            estudiante = Estudiante.objects.create(
                carnet_identidad=data['carnet'],
                nombre=data['nombre'],
                sexo=data['sexo'],
                carrera=data['carrera'],
                ano=data['ano']
            )
            estudiantes.append(estudiante)
        
        self.stdout.write(f'Creados {len(estudiantes)} estudiantes')
        
        # Crear máquinas
        maquinas_data = [
            {'nombre': 'PC-LAB-001', 'ip': '192.168.1.101', 'internet': True},
            {'nombre': 'PC-LAB-002', 'ip': '192.168.1.102', 'internet': True},
            {'nombre': 'PC-LAB-003', 'ip': '192.168.1.103', 'internet': False},
            {'nombre': 'PC-LAB-004', 'ip': '192.168.1.104', 'internet': True},
            {'nombre': 'PC-LAB-005', 'ip': '192.168.1.105', 'internet': True},
            {'nombre': 'PC-LAB-006', 'ip': '192.168.1.106', 'internet': False},
            {'nombre': 'PC-LAB-007', 'ip': '192.168.1.107', 'internet': True},
            {'nombre': 'PC-LAB-008', 'ip': '192.168.1.108', 'internet': True},
            {'nombre': 'PC-LAB-009', 'ip': '192.168.1.109', 'internet': True},
            {'nombre': 'PC-LAB-010', 'ip': '192.168.1.110', 'internet': False},
        ]
        
        maquinas = []
        for data in maquinas_data:
            maquina = Maquina.objects.create(
                nombre_red=data['nombre'],
                numero_ip=data['ip'],
                tiene_internet=data['internet']
            )
            maquinas.append(maquina)
        
        self.stdout.write(f'Creadas {len(maquinas)} máquinas')
        
        # Generar accesos de las últimas 4 semanas
        fecha_base = timezone.now() - timedelta(days=28)
        
        # Crear accesos de clase
        asignaturas = ['Calculo', 'Programacion I', 'Programacion II', 'Base de Datos', 'Redes', 'Algoritmos']
        tipos_clase = ['LAB', 'SEM', 'EP', 'EF']
        profesores = ['Dr. González', 'Dra. Martínez', 'Dr. López', 'Dra. Rodríguez', 'Dr. Fernández']
        
        accesos_clase = []
        for i in range(50):
            estudiante = random.choice(estudiantes)
            maquina = random.choice(maquinas)
            
            dias_aleatorios = random.randint(0, 28)
            fecha_entrada = fecha_base + timedelta(
                days=dias_aleatorios,
                hours=random.randint(8, 16),
                minutes=random.randint(0, 59)
            )
            
            duracion_horas = random.randint(1, 4)
            fecha_salida = fecha_entrada + timedelta(hours=duracion_horas, minutes=random.randint(0, 59))
            
            acceso = AccesoClase.objects.create(
                estudiante=estudiante,
                maquina=maquina,
                fecha_hora_entrada=fecha_entrada,
                fecha_hora_salida=fecha_salida,
                asignatura=random.choice(asignaturas),
                tipo_clase=random.choice(tipos_clase),
                profesor=random.choice(profesores)
            )
            accesos_clase.append(acceso)
        
        self.stdout.write(f'Creados {len(accesos_clase)} accesos de clase')
        
        # Crear accesos fuera de clase
        motivos = ['PROY', 'TRAB', 'OTRO']
        
        accesos_fuera = []
        for i in range(30):
            estudiante = random.choice(estudiantes)
            maquina = random.choice(maquinas)
            
            dias_aleatorios = random.randint(0, 28)
            fecha_entrada = fecha_base + timedelta(
                days=dias_aleatorios,
                hours=random.randint(17, 20),
                minutes=random.randint(0, 59)
            )
            
            duracion_minutos = random.randint(30, 180)
            fecha_salida = fecha_entrada + timedelta(minutes=duracion_minutos)
            
            acceso = AccesoFueraClase.objects.create(
                estudiante=estudiante,
                maquina=maquina,
                fecha_hora_entrada=fecha_entrada,
                fecha_hora_salida=fecha_salida,
                motivo=random.choice(motivos)
            )
            accesos_fuera.append(acceso)
        
        self.stdout.write(f'Creados {len(accesos_fuera)} accesos fuera de clase')
        
        self.stdout.write(self.style.SUCCESS('Base de datos poblada exitosamente!'))
        
        # Mostrar resumen
        self.stdout.write('\n=== RESUMEN ===')
        self.stdout.write(f'Estudiantes: {Estudiante.objects.count()}')
        self.stdout.write(f'Máquinas: {Maquina.objects.count()}')
        self.stdout.write(f'Accesos de clase: {AccesoClase.objects.count()}')
        self.stdout.write(f'Accesos fuera de clase: {AccesoFueraClase.objects.count()}')
