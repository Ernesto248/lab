# API REST - Sistema de Control de Accesos al Laboratorio

Esta documentación describe todos los endpoints disponibles en la API REST para el sistema de control de accesos del laboratorio de computación.

## Base URL

```
http://localhost:8000/api/
```

## Endpoints CRUD (Operaciones básicas)

### 1. Estudiantes

- **GET** `/api/estudiantes/` - Listar todos los estudiantes
- **GET** `/api/estudiantes/{carnet}/` - Obtener un estudiante específico
- **POST** `/api/estudiantes/` - Crear un nuevo estudiante
- **PUT** `/api/estudiantes/{carnet}/` - Actualizar un estudiante completo
- **PATCH** `/api/estudiantes/{carnet}/` - Actualizar parcialmente un estudiante
- **DELETE** `/api/estudiantes/{carnet}/` - Eliminar un estudiante

#### Ejemplo de datos para estudiante:

```json
{
  "carnet_identidad": "95032112345",
  "nombre": "Ana García López",
  "sexo": "F",
  "carrera": "Informatica",
  "ano": 3
}
```

### 2. Máquinas

- **GET** `/api/maquinas/` - Listar todas las máquinas
- **GET** `/api/maquinas/{id}/` - Obtener una máquina específica
- **POST** `/api/maquinas/` - Crear una nueva máquina
- **PUT** `/api/maquinas/{id}/` - Actualizar una máquina completa
- **PATCH** `/api/maquinas/{id}/` - Actualizar parcialmente una máquina
- **DELETE** `/api/maquinas/{id}/` - Eliminar una máquina

#### Ejemplo de datos para máquina:

```json
{
  "nombre_red": "PC-LAB-001",
  "numero_ip": "192.168.1.101",
  "tiene_internet": true
}
```

### 3. Accesos de Clase

- **GET** `/api/accesos-clase/` - Listar todos los accesos de clase
- **GET** `/api/accesos-clase/{id}/` - Obtener un acceso específico
- **POST** `/api/accesos-clase/` - Crear un nuevo acceso
- **PUT** `/api/accesos-clase/{id}/` - Actualizar un acceso completo
- **PATCH** `/api/accesos-clase/{id}/` - Actualizar parcialmente un acceso
- **DELETE** `/api/accesos-clase/{id}/` - Eliminar un acceso

#### Ejemplo de datos para acceso de clase:

```json
{
  "estudiante": "95032112345",
  "maquina": 1,
  "fecha_hora_entrada": "2024-12-01T10:00:00Z",
  "fecha_hora_salida": "2024-12-01T12:00:00Z",
  "asignatura": "Programacion I",
  "tipo_clase": "LAB",
  "profesor": "Dr. González"
}
```

### 4. Accesos Fuera de Clase

- **GET** `/api/accesos-fuera-clase/` - Listar todos los accesos fuera de clase
- **GET** `/api/accesos-fuera-clase/{id}/` - Obtener un acceso específico
- **POST** `/api/accesos-fuera-clase/` - Crear un nuevo acceso
- **PUT** `/api/accesos-fuera-clase/{id}/` - Actualizar un acceso completo
- **PATCH** `/api/accesos-fuera-clase/{id}/` - Actualizar parcialmente un acceso
- **DELETE** `/api/accesos-fuera-clase/{id}/` - Eliminar un acceso

#### Ejemplo de datos para acceso fuera de clase:

```json
{
  "estudiante": "95032112345",
  "maquina": 1,
  "fecha_hora_entrada": "2024-12-01T18:00:00Z",
  "fecha_hora_salida": "2024-12-01T20:00:00Z",
  "motivo": "PROY"
}
```

## Endpoints Personalizados

### 1. Calcular AEE (Aprovechamiento Estimado de Estancia)

- **URL**: `/api/calcular-aee/`
- **Método**: `POST`
- **Descripción**: Calcula el aprovechamiento estimado en minutos para una sesión específica

#### Entrada:

```json
{
  "carnet_identidad": "95032112345",
  "fecha_hora_entrada": "2024-12-01T10:00:00Z"
}
```

#### Salida:

```json
{
  "aprovechamiento_minutos": 102.0
}
```

#### Lógica de cálculo:

- **Laboratorio (LAB)**: 85% del tiempo total
- **Seminario (SEM)**: 90% del tiempo total
- **Evaluación Parcial (EP)**: 95% del tiempo total
- **Evaluación Final (EF)**: 98% del tiempo total
- **Proyecto (PROY)**: 80% del tiempo total
- **Trabajo extra clase (TRAB)**: 75% del tiempo total
- **Otro (OTRO)**: 60% del tiempo total

### 2. Estudiantes por Máquina y Asignatura

- **URL**: `/api/accesos-clase/por_maquina_asignatura/?maquina_id=1&asignatura=Calculo`
- **Método**: `GET`
- **Descripción**: Lista los accesos (con datos de estudiantes) filtrados por máquina y asignatura

#### Parámetros de consulta:

- `maquina_id`: ID de la máquina
- `asignatura`: Nombre de la asignatura

#### Ejemplo de URL:

```
GET /api/accesos-clase/por_maquina_asignatura/?maquina_id=1&asignatura=Programacion I
```

### 3. Estudiante por Máquina y Tiempo

- **URL**: `/api/estudiante-por-maquina-tiempo/?maquina_id=1&fecha_hora=2024-12-01T10:30:00Z`
- **Método**: `GET`
- **Descripción**: Encuentra qué estudiante estaba usando una máquina en un momento específico

#### Parámetros de consulta:

- `maquina_id`: ID de la máquina
- `fecha_hora`: Fecha y hora a consultar (formato ISO 8601)

#### Salida:

```json
{
  "carnet_identidad": "95032112345",
  "nombre": "Ana García López",
  "sexo": "F",
  "carrera": "Informatica",
  "ano": 3,
  "edad": 29
}
```

### 4. Análisis de Uso por Carrera

- **URL**: `/api/analisis/uso-por-carrera/?carrera=Informatica`
- **Método**: `GET`
- **Descripción**: Determina qué año de una carrera específica más usa el laboratorio

#### Parámetros de consulta:

- `carrera`: Nombre de la carrera

#### Salida:

```json
{
  "carrera": "Informatica",
  "ano_mas_uso": 3
}
```

### 5. Reporte de Uso Semanal

- **URL**: `/api/reportes/uso-semanal/?fecha_inicio=2024-12-01`
- **Método**: `GET`
- **Descripción**: Lista estudiantes que usaron el laboratorio en una semana específica, ordenados por edad

#### Parámetros de consulta:

- `fecha_inicio`: Fecha de inicio de la semana (formato YYYY-MM-DD)

#### Salida:

```json
[
  {
    "carnet_identidad": "04062490123",
    "nombre": "Antonio García Ramos",
    "sexo": "M",
    "carrera": "Informatica",
    "ano": 1,
    "edad": 20
  },
  {
    "carnet_identidad": "03041389012",
    "nombre": "Isabel López Vega",
    "sexo": "F",
    "carrera": "Sistemas",
    "ano": 3,
    "edad": 21
  }
]
```

## Códigos de Estado HTTP

- **200 OK**: Solicitud exitosa
- **201 Created**: Recurso creado exitosamente
- **400 Bad Request**: Error en los datos enviados
- **404 Not Found**: Recurso no encontrado
- **500 Internal Server Error**: Error interno del servidor

## Paginación

Los endpoints de listado incluyen paginación automática:

- **page_size**: 20 elementos por página
- **Parámetros**: `?page=2` para navegar entre páginas

## Formato de Fechas

Todas las fechas deben enviarse en formato ISO 8601:

```
YYYY-MM-DDTHH:MM:SSZ
```

Ejemplo: `2024-12-01T10:30:00Z`

## Browsable API

Django REST Framework incluye una interfaz web navegable. Accede a cualquier endpoint desde el navegador para ver la documentación interactiva y probar los endpoints:

```
http://localhost:8000/api/
```

## Ejemplos con cURL

### Crear un estudiante:

```bash
curl -X POST http://localhost:8000/api/estudiantes/ \
  -H "Content-Type: application/json" \
  -d '{
    "carnet_identidad": "05071234567",
    "nombre": "Nuevo Estudiante",
    "sexo": "M",
    "carrera": "Informatica",
    "ano": 2
  }'
```

### Calcular AEE:

```bash
curl -X POST http://localhost:8000/api/calcular-aee/ \
  -H "Content-Type: application/json" \
  -d '{
    "carnet_identidad": "95032112345",
    "fecha_hora_entrada": "2024-12-01T10:00:00Z"
  }'
```

### Buscar estudiante por máquina y tiempo:

```bash
curl "http://localhost:8000/api/estudiante-por-maquina-tiempo/?maquina_id=1&fecha_hora=2024-12-01T10:30:00Z"
```
