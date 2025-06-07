from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    EstudianteViewSet, MaquinaViewSet, AccesoClaseViewSet, AccesoFueraClaseViewSet,
    calcular_aee, estudiante_por_maquina_tiempo, uso_por_carrera, uso_semanal
)

# Crear el router y registrar los viewsets
router = DefaultRouter()
router.register(r'estudiantes', EstudianteViewSet)
router.register(r'maquinas', MaquinaViewSet)
router.register(r'accesos-clase', AccesoClaseViewSet)
router.register(r'accesos-fuera-clase', AccesoFueraClaseViewSet)

urlpatterns = [
    # Endpoints personalizados (deben ir antes que las URLs del router)
    path('api/calcular-aee/', calcular_aee, name='calcular-aee'),
    path('api/estudiante-por-maquina-tiempo/', estudiante_por_maquina_tiempo, name='estudiante-por-maquina-tiempo'),
    path('api/analisis/uso-por-carrera/', uso_por_carrera, name='uso-por-carrera'),
    path('api/reportes/uso-semanal/', uso_semanal, name='uso-semanal'),
    
    # URLs del router (CRUD completo)
    path('api/', include(router.urls)),
]
