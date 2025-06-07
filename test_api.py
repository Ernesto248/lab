#!/usr/bin/env python3
"""
Script de pruebas para la API REST del Sistema de Control de Accesos
Ejecutar desde el directorio del proyecto: python test_api.py
"""

import requests
import json
from datetime import datetime, timedelta

# Configuración
BASE_URL = "http://localhost:8000/api"
headers = {'Content-Type': 'application/json'}

def test_endpoint(method, endpoint, data=None, params=None):
    """Función auxiliar para probar endpoints"""
    url = f"{BASE_URL}{endpoint}"
    
    print(f"\n{'='*60}")
    print(f"Probando: {method} {endpoint}")
    print(f"URL completa: {url}")
    
    if params:
        print(f"Parámetros: {params}")
    
    if data:
        print(f"Datos enviados: {json.dumps(data, indent=2)}")
    
    try:
        if method == 'GET':
            response = requests.get(url, params=params)
        elif method == 'POST':
            response = requests.post(url, json=data, headers=headers)
        elif method == 'PUT':
            response = requests.put(url, json=data, headers=headers)
        elif method == 'DELETE':
            response = requests.delete(url)
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code < 400:
            try:
                result = response.json()
                print(f"Respuesta exitosa:")
                print(json.dumps(result, indent=2, ensure_ascii=False))
                return result
            except json.JSONDecodeError:
                print("Respuesta sin contenido JSON")
                return None
        else:
            print(f"Error: {response.text}")
            return None
            
    except requests.exceptions.ConnectionError:
        print("Error: No se puede conectar al servidor. ¿Está ejecutándose Django?")
        return None
    except Exception as e:
        print(f"Error inesperado: {e}")
        return None

def main():
    print("🚀 PRUEBAS DE LA API REST - SISTEMA DE CONTROL DE ACCESOS")
    print("Asegúrate de que el servidor Django esté ejecutándose en http://localhost:8000")
    
    # 1. Probar endpoints CRUD básicos
    print(f"\n{'🔥' * 20} ENDPOINTS CRUD BÁSICOS {'🔥' * 20}")
    
    # Listar estudiantes
    estudiantes = test_endpoint('GET', '/estudiantes/')
    
    # Listar máquinas
    maquinas = test_endpoint('GET', '/maquinas/')
    
    # Listar accesos de clase
    accesos_clase = test_endpoint('GET', '/accesos-clase/')
    
    # Listar accesos fuera de clase
    accesos_fuera = test_endpoint('GET', '/accesos-fuera-clase/')
    
    # 2. Crear un nuevo estudiante
    print(f"\n{'🆕' * 20} CREAR NUEVO ESTUDIANTE {'🆕' * 20}")
    nuevo_estudiante = {
        "carnet_identidad": "05071234567",
        "nombre": "Estudiante de Prueba",
        "sexo": "M",
        "carrera": "Informatica",
        "ano": 2
    }
    test_endpoint('POST', '/estudiantes/', data=nuevo_estudiante)
    
    # 3. Obtener el estudiante creado
    test_endpoint('GET', '/estudiantes/05071234567/')
    
    # 4. Probar endpoints personalizados
    print(f"\n{'⚡' * 20} ENDPOINTS PERSONALIZADOS {'⚡' * 20}")
    
    if accesos_clase and len(accesos_clase.get('results', [])) > 0:
        # Usar datos reales de la base de datos
        primer_acceso = accesos_clase['results'][0]
        carnet_ejemplo = primer_acceso['estudiante']
        fecha_ejemplo = primer_acceso['fecha_hora_entrada']
        maquina_ejemplo = primer_acceso['maquina']
        asignatura_ejemplo = primer_acceso['asignatura']
        
        # Calcular AEE
        print(f"\n{'💡' * 15} CALCULAR AEE {'💡' * 15}")
        aee_data = {
            "carnet_identidad": carnet_ejemplo,
            "fecha_hora_entrada": fecha_ejemplo
        }
        test_endpoint('POST', '/calcular-aee/', data=aee_data)
        
        # Estudiantes por máquina y asignatura
        print(f"\n{'🔍' * 15} ESTUDIANTES POR MÁQUINA Y ASIGNATURA {'🔍' * 15}")
        params = {
            'maquina_id': maquina_ejemplo,
            'asignatura': asignatura_ejemplo
        }
        test_endpoint('GET', '/accesos-clase/por_maquina_asignatura/', params=params)
        
        # Estudiante por máquina y tiempo
        print(f"\n{'⏰' * 15} ESTUDIANTE POR MÁQUINA Y TIEMPO {'⏰' * 15}")
        # Usar la fecha de entrada del acceso
        params = {
            'maquina_id': maquina_ejemplo,
            'fecha_hora': fecha_ejemplo
        }
        test_endpoint('GET', '/estudiante-por-maquina-tiempo/', params=params)
    
    # Análisis de uso por carrera
    print(f"\n{'📊' * 15} ANÁLISIS DE USO POR CARRERA {'📊' * 15}")
    test_endpoint('GET', '/analisis/uso-por-carrera/', params={'carrera': 'Informatica'})
    
    # Reporte de uso semanal
    print(f"\n{'📅' * 15} REPORTE DE USO SEMANAL {'📅' * 15}")
    fecha_semana = (datetime.now() - timedelta(days=7)).date().isoformat()
    test_endpoint('GET', '/reportes/uso-semanal/', params={'fecha_inicio': fecha_semana})
    
    # 5. Probar casos de error
    print(f"\n{'❌' * 20} CASOS DE ERROR {'❌' * 20}")
    
    # Estudiante no encontrado
    test_endpoint('GET', '/estudiantes/99999999999/')
    
    # AEE con datos inválidos
    test_endpoint('POST', '/calcular-aee/', data={
        "carnet_identidad": "inexistente",
        "fecha_hora_entrada": "2024-01-01T00:00:00Z"
    })
    
    # Parámetros faltantes
    test_endpoint('GET', '/estudiante-por-maquina-tiempo/', params={'maquina_id': 1})
    
    print(f"\n{'✅' * 20} PRUEBAS COMPLETADAS {'✅' * 20}")
    print("\n📝 Revisa los resultados arriba para verificar que todos los endpoints funcionen correctamente.")
    print("\n🌐 También puedes probar la API navegable en: http://localhost:8000/api/")

if __name__ == "__main__":
    main()
