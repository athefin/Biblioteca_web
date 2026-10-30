from django import forms
from Biblioteca_web.models import Estudiante, RecursoFisico, ReporteIncidencia

class EstudianteForm(forms.ModelForm):
    class Meta:
        model = Estudiante
        fields = ['rut', 'nombre', 'carrera']
        widgets = {
            'rut': forms.TextInput(attrs={'class': 'form-control'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'carrera': forms.TextInput(attrs={'class': 'form-control'}),
        }

class RecursoFisicoForm(forms.ModelForm):
    class Meta:
        model = RecursoFisico
        fields = ['identificador', 'tipo', 'estado']
        widgets = {
            'identificador': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo': forms.Select(attrs={'class': 'form-control'}),
            'estado': forms.Select(attrs={'class': 'form-control'}),
        }

class ReporteIncidenciaForm(forms.ModelForm):
    class Meta:
        model = ReporteIncidencia
        fields = ['recurso', 'estudiante', 'descripcion_falla']
        widgets = {
            'recurso': forms.Select(attrs={'class': 'form-control'}),
            'estudiante': forms.Select(attrs={'class': 'form-control'}),
            'descripcion_falla': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }