from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Estudiante(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    rut = models.CharField(max_length=12, unique=True, verbose_name="RUT del Estudiante")
    nombre = models.CharField(max_length=100)
    carrera = models.CharField(max_length=100)

    class Meta:
        app_label = 'Biblioteca_web'

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

    class Meta:
        app_label = 'Biblioteca_web'

    def __str__(self):
        fila = 'Recurso: ' + self.tipo + ' - ID: ' + self.identificador + ' - Estado: ' + self.estado
        return fila

class ReporteIncidencia(models.Model):
    recurso = models.ForeignKey(RecursoFisico, on_delete=models.CASCADE)
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE)
    descripcion_falla = models.TextField(verbose_name="Detalle de la falla") 
    fecha_reporte = models.DateTimeField(auto_now_add=True)
    resuelto = models.BooleanField(default=False)

    class Meta:
        app_label = 'Biblioteca_web'

    def __str__(self):
        fila = 'Reporte de ' + self.recurso.identificador + ' por ' + self.estudiante.rut
        return fila
    
class Reserva(models.Model):
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE)
    sala = models.ForeignKey('RecursoFisico', on_delete=models.CASCADE)
    fecha = models.DateField()
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    activa = models.BooleanField(default=True)
 

class Libro(models.Model):
    titulo = models.CharField(max_length=200)
    autor = models.CharField(max_length=100)
    class Meta:
        app_label = 'Biblioteca_web'
    def __str__(self):
        return f"{self.titulo} - {self.autor}"

class Reseña(models.Model):
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE)
    libro = models.ForeignKey(Libro, on_delete=models.CASCADE)
    texto = models.TextField()
    aprobada = models.BooleanField(default=True)
    fecha = models.DateTimeField(auto_now_add=True)