#!/usr/bin/env python3
import os
import sys
import django

# Configure Django settings
sys.path.append('c:\\Users\\mleon\\code\\lab')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'laboratorio_accesos.settings')
django.setup()

from accesos.models import AccesoClase, Maquina

def check_data():
    print("=== Datos disponibles para testing ===")
    
    # Check asignaturas
    asignaturas = AccesoClase.objects.values_list('asignatura', flat=True).distinct()
    print("Asignaturas disponibles:")
    for asignatura in asignaturas:
        print(f"  - {asignatura}")
    
    # Check maquinas
    maquinas = Maquina.objects.all()
    print(f"\nMáquinas disponibles ({len(maquinas)} total):")
    for maquina in maquinas[:5]:  # Show first 5
        print(f"  - ID: {maquina.id}, Nombre: {maquina.nombre}")
    
    # Check some sample data
    first_acceso = AccesoClase.objects.first()
    if first_acceso:
        print(f"\nEjemplo de acceso:")
        print(f"  - Máquina ID: {first_acceso.maquina.id}")
        print(f"  - Asignatura: {first_acceso.asignatura}")
        print(f"  - Estudiante: {first_acceso.estudiante.nombre}")

if __name__ == "__main__":
    check_data()
