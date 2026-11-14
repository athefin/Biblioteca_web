import os
import sys
import django

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)
sys.path.append(os.path.dirname(BASE_DIR))
sys.path.append(os.path.dirname(os.path.dirname(BASE_DIR)))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
django.setup()

from Biblioteca_web.models import Estudiante, Libro, RecursoFisico

def poblar_base_de_datos():
    print("Creando estudiantes...")
    estudiantes = [
        {'rut': '21.111.111-1', 'nombre': 'Samy Contreras', 'carrera': 'Ingeniería en Informática'},
        {'rut': '22.222.222-2', 'nombre': 'Valentina Soto', 'carrera': 'Ingeniería en Informática'},
        {'rut': '23.333.333-3', 'nombre': 'Matías Torres', 'carrera': 'Analista Programador'},
        {'rut': '24.444.444-4', 'nombre': 'Camila Rojas', 'carrera': 'Administración de Empresas'},
        {'rut': '25.555.555-5', 'nombre': 'Diego Muñoz', 'carrera': 'Mecánica Automotriz'},
    ]
    
    for est in estudiantes:
        # Aquí pasamos únicamente los campos que existen en models.py sin meter 'is_active'
        Estudiante.objects.get_or_create(
            rut=est['rut'], 
            defaults={
                'nombre': est['nombre'], 
                'carrera': est['carrera']
            }
        )

    print("Creando recursos físicos...")
    recursos = [
        {'identificador': 'P1 001', 'tipo': 'PC', 'estado': 'DISPONIBLE'},
        {'identificador': 'P1 002', 'tipo': 'PC', 'estado': 'DISPONIBLE'},
        {'identificador': 'P1 003', 'tipo': 'PC', 'estado': 'OCUPADO'},
        {'identificador': 'P1 004', 'tipo': 'PC', 'estado': 'MANTENCION'},
        {'identificador': 'P1 005', 'tipo': 'PC', 'estado': 'DISPONIBLE'},
        {'identificador': 'P2 001', 'tipo': 'PC', 'estado': 'DISPONIBLE'},
        {'identificador': 'P2 002', 'tipo': 'PC', 'estado': 'OCUPADO'},
        {'identificador': 'P2 003', 'tipo': 'PC', 'estado': 'DISPONIBLE'},
        {'identificador': 'P2 004', 'tipo': 'PC', 'estado': 'MANTENCION'},
        {'identificador': 'Sala 1', 'tipo': 'SALA', 'estado': 'DISPONIBLE'},
        {'identificador': 'Sala 2', 'tipo': 'SALA', 'estado': 'OCUPADO'},
    ]

    for rec in recursos:
        RecursoFisico.objects.get_or_create(
            identificador=rec['identificador'], 
            defaults={
                'tipo': rec['tipo'], 
                'estado': rec['estado']
            }
        )
        
    print("Creando libros...")
    libros = [
        {'titulo': 'Base de Datos Avanzadas', 'autor': 'Abraham Silberschatz'},
        {'titulo': 'Clean Code', 'autor': 'Robert C. Martin'},
        {'titulo': 'El Arte de la Intrusión', 'autor': 'Kevin Mitnick'},
        {'titulo': 'Patrones de Diseño', 'autor': 'Erich Gamma'},
    ]
    for lib in libros:
        Libro.objects.get_or_create(titulo=lib['titulo'], defaults=lib)
        
        print("¡Base de datos poblada con éxito!")

if __name__ == '__main__':
    poblar_base_de_datos()