# Create your views here.
from django.shortcuts import render, redirect
from Biblioteca_web.models import Estudiante, RecursoFisico, ReporteIncidencia
from Biblioteca_web.forms import EstudianteForm, RecursoFisicoForm, ReporteIncidenciaForm

#VISTAS PARA ESTUDIANTES
def lista_estudiantes(request):
    estudiantes = Estudiante.objects.all()
    return render(request, 'lista_estudiantes.html', {'estudiantes': estudiantes})

def crear_estudiante(request):
    if request.method == 'POST':
        form = EstudianteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_estudiantes')
    else:
        form = EstudianteForm()
    return render(request, 'crear_estudiante.html', {'form': form})

#VISTAS PARA RECURSOS
def lista_recursos(request):
    recursos = RecursoFisico.objects.all()
    return render(request, 'lista_recursos.html', {'recursos': recursos})

def crear_recurso(request):
    if request.method == 'POST':
        form = RecursoFisicoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_recursos')
    else:
        form = RecursoFisicoForm()
    return render(request, 'crear_recurso.html', {'form': form})

#VISTAS PARA REPORTES
def lista_reportes(request):
    reportes = ReporteIncidencia.objects.all()
    return render(request, 'lista_reportes.html', {'reportes': reportes})

def crear_reporte(request):
    if request.method == 'POST':
        form = ReporteIncidenciaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_reportes')
    else:
        form = ReporteIncidenciaForm()
    return render(request, 'crear_reporte.html', {'form': form})