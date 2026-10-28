from django.db import models

# Create your models here.
class Estudiante(models.Model):
    rut = models.CharField(max_length=12, unique=True, verbose_name="RUT del Estudiante") # Control de integridad con RUT
    nombre = models.CharField(max_length=100)
    carrera = models.CharField(max_length=100)

    def __str__(self):
        fila = 'Estudiante: ' + self.nombre + ' - RUT: ' + self.rut
        return fila

class RecursoFisico(models.Model):
    TIPO_CHOICES = [
        ('PC', 'Computador'),
        ('SALA', 'Sala de Estudio'),
    ]
    ESTADO_CHOICES = [
        ('DISPONIBLE', 'Disponible'),
        ('OCUPADO', 'Ocupado'),
        ('MANTENCION', 'En Mantención'),
    ]
    identificador = models.CharField(max_length=50, unique=True, verbose_name="Número de Equipo/Sala") 
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='DISPONIBLE')

    def __str__(self):
        fila = 'Recurso: ' + self.tipo + ' - ID: ' + self.identificador + ' - Estado: ' + self.estado
        return fila

class ReporteIncidencia(models.Model):
    recurso = models.ForeignKey(RecursoFisico, on_delete=models.CASCADE)
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE) # Trazabilidad del reporte
    descripcion_falla = models.TextField(verbose_name="Detalle de la falla") 
    fecha_reporte = models.DateTimeField(auto_now_add=True)
    resuelto = models.BooleanField(default=False)

    def __str__(self):
        fila = 'Reporte de ' + self.recurso.identificador + ' por ' + self.estudiante.rut
        return fila