#!/usr/bin/env python3
"""
Script para probar el endpoint por-maquina-asignatura específicamente
"""
import requests
import json

BASE_URL = "http://127.0.0.1:8000"

def test_por_maquina_asignatura():
    """Probar el endpoint por-maquina-asignatura con diferentes URLs"""
    
    # URLs posibles a probar
    urls_to_test = [
        f"{BASE_URL}/api/accesos-clase/por-maquina-asignatura/",
        f"{BASE_URL}/api/accesos-clase/por_maquina_asignatura/",
        f"{BASE_URL}/api/accesos-clase/por-maquina-asignatura/?maquina_id=1&asignatura=Programacion",
        f"{BASE_URL}/api/accesos-clase/por_maquina_asignatura/?maquina_id=1&asignatura=Programacion"
    ]
    
    for url in urls_to_test:
        try:
            print(f"\n--- Probando URL: {url} ---")
            response = requests.get(url, timeout=10)
            print(f"Status Code: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ SUCCESS - Datos recibidos: {len(data) if isinstance(data, list) else 'objeto'}")
                if isinstance(data, list) and len(data) > 0:
                    print(f"Primer resultado: {json.dumps(data[0], indent=2, ensure_ascii=False)}")
                elif isinstance(data, dict):
                    print(f"Resultado: {json.dumps(data, indent=2, ensure_ascii=False)}")
                break
            else:
                print(f"❌ Error: {response.status_code}")
                try:
                    error_data = response.json()
                    print(f"Error details: {json.dumps(error_data, indent=2, ensure_ascii=False)}")
                except:
                    print(f"Error text: {response.text}")
                    
        except requests.exceptions.RequestException as e:
            print(f"❌ Request failed: {e}")
            
    print("\n" + "="*50)

if __name__ == "__main__":
    print("Probando endpoint por-maquina-asignatura...")
    test_por_maquina_asignatura()
