from django.db import models
from datetime import datetime, date


class Estudiante(models.Model):
    SEXO_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Femenino'),
    ]
    
    carnet_identidad = models.CharField(max_length=11, primary_key=True)
    nombre = models.CharField(max_length=100)
    sexo = models.CharField(max_length=10, choices=SEXO_CHOICES)
    carrera = models.CharField(max_length=50)
    ano = models.IntegerField(verbose_name='Año')
    
    @property
    def edad(self):
        """Calcula la edad basada en los primeros 6 dígitos del carnet (AAMMDD)"""
        try:
            # Extraer los primeros 6 dígitos del carnet
            fecha_str = self.carnet_identidad[:6]
            # Asumir formato AAMMDD
            ano_nacimiento = int('19' + fecha_str[:2])  # Asumiendo años 19XX
            mes_nacimiento = int(fecha_str[2:4])
            dia_nacimiento = int(fecha_str[4:6])
            
            # Si el año es menor a 50, asumir 20XX
            if int(fecha_str[:2]) < 50:
                ano_nacimiento = int('20' + fecha_str[:2])
            
            fecha_nacimiento = date(ano_nacimiento, mes_nacimiento, dia_nacimiento)
            hoy = date.today()
            edad = hoy.year - fecha_nacimiento.year
            
            # Ajustar si no ha cumplido años este año
            if hoy.month < fecha_nacimiento.month or (hoy.month == fecha_nacimiento.month and hoy.day < fecha_nacimiento.day):
                edad -= 1
                
            return edad
        except (ValueError, IndexError):
            return None
    
    class Meta:
        verbose_name_plural = "Estudiantes"
    
    def __str__(self):
        return f"{self.nombre} - {self.carnet_identidad}"


class Maquina(models.Model):
    nombre_red = models.CharField(max_length=50, unique=True)
    numero_ip = models.GenericIPAddressField(unique=True)
    tiene_internet = models.BooleanField(default=True)
    
    class Meta:
        verbose_name_plural = "Máquinas"
    
    def __str__(self):
        return f"{self.nombre_red} - {self.numero_ip}"


class AccesoClase(models.Model):
    TIPO_CLASE_CHOICES = [
        ('LAB', 'Laboratorio'),
        ('SEM', 'Seminario'),
        ('EP', 'Evaluación parcial'),
        ('EF', 'Evaluación final'),
    ]
    
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE)
    maquina = models.ForeignKey(Maquina, on_delete=models.CASCADE)
    fecha_hora_entrada = models.DateTimeField()
    fecha_hora_salida = models.DateTimeField(null=True, blank=True)
    asignatura = models.CharField(max_length=100)
    tipo_clase = models.CharField(max_length=3, choices=TIPO_CLASE_CHOICES)
    profesor = models.CharField(max_length=100)
    
    class Meta:
        verbose_name_plural = "Accesos en Clase"
    
    def __str__(self):
        return f"{self.estudiante.nombre} - {self.maquina.nombre_red} - {self.asignatura}"


class AccesoFueraClase(models.Model):
    MOTIVO_CHOICES = [
        ('PROY', 'Proyecto'),
        ('TRAB', 'Trabajo extra clase'),
        ('OTRO', 'Otro'),
    ]
    
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE)
    maquina = models.ForeignKey(Maquina, on_delete=models.CASCADE)
    fecha_hora_entrada = models.DateTimeField()
    fecha_hora_salida = models.DateTimeField(null=True, blank=True)
    motivo = models.CharField(max_length=4, choices=MOTIVO_CHOICES)
    
    class Meta:
        verbose_name_plural = "Accesos Fuera de Clase"
    
    def __str__(self):
        return f"{self.estudiante.nombre} - {self.maquina.nombre_red} - {self.motivo}"
