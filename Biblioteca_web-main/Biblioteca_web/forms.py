from django import forms
from Biblioteca_web.models import Estudiante, RecursoFisico, ReporteIncidencia, Reserva, Reseña 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

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
        fields = ['recurso', 'descripcion_falla']
        widgets = {
            'recurso': forms.Select(attrs={'class': 'form-control'}),
            'descripcion_falla': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
        
        

    
    
class RegistroEstudianteForm(UserCreationForm):
    rut = forms.CharField(max_length=12, label="RUT")
    nombre = forms.CharField(max_length=100, label="Nombre completo")
    carrera = forms.CharField(max_length=100, label="Carrera")
    email = forms.EmailField(label="Correo institucional")

    class Meta:
        model = User
        fields = ('email', 'rut', 'nombre', 'carrera', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(username=email).exists() or User.objects.filter(email=email).exists():
            raise forms.ValidationError("Este correo ya está registrado. Por favor, inicia sesión o usa otro correo.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['email']
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            Estudiante.objects.create(
                user=user, rut=self.cleaned_data['rut'],
                nombre=self.cleaned_data['nombre'], carrera=self.cleaned_data['carrera']
            )
        return user
    
    

class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ['sala', 'fecha', 'hora_inicio', 'hora_fin']
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'hora_inicio': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'hora_fin': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'sala': forms.Select(attrs={'class': 'form-control'}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['sala'].queryset = RecursoFisico.objects.filter(tipo='SALA', estado='DISPONIBLE')

class ResenaForm(forms.ModelForm):
    class Meta:
        model = Reseña
        fields = ['libro', 'texto']
        widgets = {
            'libro': forms.Select(attrs={'class': 'form-control'}),
            'texto': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }