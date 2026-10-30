"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from Biblioteca_web import views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    #Rutas de Estudiantes
    path('', views.lista_estudiantes, name='lista_estudiantes'),
    path('estudiante/crear/', views.crear_estudiante, name='crear_estudiante'),
    
    #Rutas de Recursos
    path('recursos/', views.lista_recursos, name='lista_recursos'),
    path('recursos/crear/', views.crear_recurso, name='crear_recurso'),
    
    #Rutas de Reportes
    path('reportes/', views.lista_reportes, name='lista_reportes'),
    path('reportes/crear/', views.crear_reporte, name='crear_reporte'),
]