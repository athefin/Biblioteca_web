from django.contrib import admin
from Biblioteca_web.models import Estudiante, RecursoFisico, ReporteIncidencia

@admin.register(Estudiante)
class EstudianteAdmin(admin.ModelAdmin):
    list_display = ('rut', 'nombre', 'carrera')
    search_fields = ('rut', 'nombre')

@admin.register(RecursoFisico)
class RecursoFisicoAdmin(admin.ModelAdmin):
    list_display = ('identificador', 'tipo', 'estado')
    list_filter = ('tipo', 'estado')

@admin.register(ReporteIncidencia)
class ReporteIncidenciaAdmin(admin.ModelAdmin):
    list_display = ('recurso', 'estudiante', 'fecha_reporte', 'resuelto')
    list_filter = ('resuelto', 'fecha_reporte')
# Register your models here.