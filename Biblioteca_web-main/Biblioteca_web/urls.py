from django.contrib import admin
from django.urls import path
from Biblioteca_web import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('registro/', views.registro_estudiante, name='registro'),
    path('', views.lista_estudiantes, name='lista_estudiantes'),
    path('estudiante/crear/', views.crear_estudiante, name='crear_estudiante'),
    path('recursos/', views.lista_recursos, name='lista_recursos'),
    path('recursos/crear/', views.crear_recurso, name='crear_recurso'),
    path('recursos/reservar/<int:recurso_id>/', views.reservar_recurso, name='reservar_recurso'),
    path('recursos/liberar/<int:recurso_id>/', views.liberar_recurso, name='liberar_recurso'),
    path('reservar-sala/', views.crear_reserva, name='crear_reserva'),
    path('reportes/', views.lista_reportes, name='lista_reportes'),
    path('reportes/crear/', views.crear_reporte, name='crear_reporte'),
    path('resenas/crear/', views.crear_resena, name='crear_resena'),
    path('resenas/eliminar/<int:resena_id>/', views.eliminar_resena, name='eliminar_resena'),
    path('poblar/', views.poblar_bd, name='poblar_bd'),
    path('libros/', views.lista_libros, name='lista_libros'),
]