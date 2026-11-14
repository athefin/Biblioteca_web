import unicodedata
import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import HttpResponse
from Biblioteca_web.models import Estudiante, Libro, RecursoFisico, ReporteIncidencia, Reserva, Reseña
from Biblioteca_web.forms import EstudianteForm, RecursoFisicoForm, ReporteIncidenciaForm, RegistroEstudianteForm, ReservaForm, ResenaForm


def obtener_o_crear_estudiante(user):
    if not user.is_authenticated:
        return None
    estudiante, created = Estudiante.objects.get_or_create(
        user=user,
        defaults={
            'rut': f"USR-{user.id}",
            'nombre': user.first_name if user.first_name else user.username,
            'carrera': 'Por definir'
        }
    )
    return estudiante

def limpiar_texto(texto):
    texto_norm = unicodedata.normalize('NFD', texto.lower().strip())
    return ''.join(c for c in texto_norm if unicodedata.category(c) != 'Mn')


def inicializar_datos_demo():
    cuentas = [
        ('Estudiante', 'estudiante_demo', 'estudiante@inacapmail.cl', '1234'),
        ('Administrativo', 'admin_biblioteca', 'admin@inacap.cl', '1234'),
        ('Soporte TI', 'soporte_ti', 'ti@inacap.cl', '1234'),
    ]
    for rol_nombre, username, email, password in cuentas:
        grupo, _ = Group.objects.get_or_create(name=rol_nombre)
        user, creado = User.objects.get_or_create(
            username=username,
            defaults={'email': email}
        )
        if creado or user.email != email:
            user.email = email
            user.set_password(password)
            user.save()
        if not user.groups.filter(name=rol_nombre).exists():
            user.groups.add(grupo)

    if RecursoFisico.objects.count() == 0:
        recursos_iniciales = [
            ('P1-PC01', 'PC', 'DISPONIBLE'),
            ('P1-PC02', 'PC', 'DISPONIBLE'),
            ('P1-PC03', 'PC', 'OCUPADO'),
            ('P2-PC01', 'PC', 'DISPONIBLE'),
            ('SALA-01', 'SALA', 'DISPONIBLE'),
            ('SALA-02', 'SALA', 'MANTENCION'),
        ]
        for ident, tipo, estado in recursos_iniciales:
            RecursoFisico.objects.create(identificador=ident, tipo=tipo, estado=estado)

    if Estudiante.objects.count() == 0:
        Estudiante.objects.create(rut='21.345.678-9', nombre='Camila Rojas', carrera='Ingeniería en Informática')
        Estudiante.objects.create(rut='20.987.654-3', nombre='Matías Soto', carrera='Analista Programador')


def obtener_rol(user):
    if not user.is_authenticated:
        return None
    for nombre_rol in ['Administrativo', 'Soporte TI', 'Estudiante']:
        if user.groups.filter(name=nombre_rol).exists():
            return nombre_rol
    return None


def redirigir_segun_rol(user):
    rol = obtener_rol(user)
    if rol == 'Administrativo':
        return redirect('lista_estudiantes')
    elif rol == 'Soporte TI':
        return redirect('lista_reportes')
    elif rol == 'Estudiante':
        return redirect('lista_recursos')
    return None


def login_view(request):
    inicializar_datos_demo()

    if request.user.is_authenticated:
        destino = redirigir_segun_rol(request.user)
        if destino:
            return destino
        logout(request)

    if request.method == 'POST':
        rol_elegido = request.POST.get('rol')
        correo = request.POST.get('correo', '').strip().lower()
        password = request.POST.get('password', '')

        usuario_bd = User.objects.filter(email__iexact=correo).first()

        if not usuario_bd:
            messages.error(request, "No existe ninguna cuenta registrada con ese correo institucional.")
            return render(request, 'login.html')

        user = authenticate(request, username=usuario_bd.username, password=password)
        if user is None:
            messages.error(request, "Contraseña incorrecta. Inténtalo nuevamente.")
            return render(request, 'login.html')

        if not user.groups.filter(name=rol_elegido).exists():
            messages.error(request, "Tu cuenta ({}) no tiene permisos para entrar como {}.".format(correo, rol_elegido))
            return render(request, 'login.html')

        login(request, user)
        return redirigir_segun_rol(user)

    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def lista_estudiantes(request):
    if request.user.groups.filter(name='Estudiante').exists():
        return redirect('lista_recursos')
    if request.user.groups.filter(name='Soporte TI').exists():
        return redirect('lista_reportes')
    estudiantes = Estudiante.objects.all()
    return render(request, 'lista_estudiantes.html', {'estudiantes': estudiantes})

@login_required(login_url='/login/')
def crear_estudiante(request):
    if obtener_rol(request.user) != 'Administrativo':
        destino = redirigir_segun_rol(request.user)
        return destino if destino else redirect('login')
    if request.method == 'POST':
        form = EstudianteForm(request.POST)
        if form.is_valid():
            estudiante = form.save()
            partes = limpiar_texto(estudiante.nombre).split()
            base_correo = '.'.join(partes[:2]) if len(partes) >= 2 else partes[0]
            correo = '{}@inacapmail.cl'.format(base_correo)
            contador = 1
            while User.objects.filter(email__iexact=correo).exists():
                correo = '{}{}@inacapmail.cl'.format(base_correo, contador)
                contador += 1

            grupo_est, _ = Group.objects.get_or_create(name='Estudiante')
            user = User.objects.create_user(
                username=correo,
                email=correo,
                password='1234',
                first_name=estudiante.nombre
            )
            user.groups.add(grupo_est)
            messages.success(
                request,
                'Estudiante creado. Login habilitado -> Correo: {} | Clave: 1234'.format(correo)
            )
            return redirect('lista_estudiantes')
    else:
        form = EstudianteForm()
    return render(request, 'crear_estudiante.html', {'form': form})

'''
@login_required(login_url='/login/')
def lista_recursos(request):
    if obtener_rol(request.user) not in ['Administrativo', 'Estudiante']:
        destino = redirigir_segun_rol(request.user)
        return destino if destino else redirect('login')
    recursos = RecursoFisico.objects.all()
    return render(request, 'lista_recursos.html', {'recursos': recursos})
'''


@login_required(login_url='/login/')
def lista_recursos(request):
    if obtener_rol(request.user) not in ['Administrativo', 'Estudiante']:
        destino = redirigir_segun_rol(request.user)
        return destino if destino else redirect('login')
    recursos = RecursoFisico.objects.all()
    estudiante = obtener_o_crear_estudiante(request.user)
    my_reserved_ids = []
    has_active_reservation = False
    if estudiante:
        reservas_activas = Reserva.objects.filter(estudiante=estudiante, activa=True)
        if reservas_activas.exists():
            has_active_reservation = True
            my_reserved_ids = list(reservas_activas.values_list('sala_id', flat=True)) 
    return render(request, 'lista_recursos.html', {
        'recursos': recursos,
        'my_reserved_ids': my_reserved_ids,
        'has_active_reservation': has_active_reservation
    })
    

@login_required(login_url='/login/')
def crear_recurso(request):
    if obtener_rol(request.user) != 'Administrativo':
        destino = redirigir_segun_rol(request.user)
        return destino if destino else redirect('login')
    if request.method == 'POST':
        form = RecursoFisicoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_recursos')
    else:
        form = RecursoFisicoForm()
    return render(request, 'crear_recurso.html', {'form': form})

'''
@login_required(login_url='/login/')
def reservar_recurso(request, recurso_id):
    if obtener_rol(request.user) not in ['Estudiante', 'Administrativo']:
        destino = redirigir_segun_rol(request.user)
        return destino if destino else redirect('login')
    if request.method == 'POST':
        with transaction.atomic():
            recurso = get_object_or_404(RecursoFisico.objects.select_for_update(), id=recurso_id)
            if recurso.estado != 'DISPONIBLE':
                messages.error(
                    request,
                    'La sala {} ya está ocupada o no disponible. Selecciona otra sala libre.'.format(recurso.identificador)
                )
                return redirect('lista_recursos')
            recurso.estado = 'OCUPADO'
            recurso.save()
            messages.success(
                request,
                '¡Reserva confirmada! {} quedó bloqueada a tu nombre.'.format(recurso.identificador)
            )
    return redirect('lista_recursos')
'''


@login_required(login_url='/login/')
def reservar_recurso(request, recurso_id):
    if obtener_rol(request.user) not in ['Estudiante', 'Administrativo']:
        return redirect('login')
    if request.method == 'POST':
        estudiante = obtener_o_crear_estudiante(request.user)
        if Reserva.objects.filter(estudiante=estudiante, activa=True).exists():
            messages.error(request, "Ya tienes una reserva activa. Debes liberarla antes de reservar otro equipo.")
            return redirect('lista_recursos')
        with transaction.atomic():
            recurso = get_object_or_404(RecursoFisico.objects.select_for_update(), id=recurso_id)
            if recurso.estado != 'DISPONIBLE':
                messages.error(request, f'El recurso {recurso.identificador} ya está ocupado.')
                return redirect('lista_recursos')
            recurso.estado = 'OCUPADO'
            recurso.save()
            ahora = datetime.datetime.now()
            Reserva.objects.create(
                estudiante=estudiante,
                sala=recurso,
                fecha=ahora.date(),
                hora_inicio=ahora.time(),
                hora_fin=(ahora + datetime.timedelta(hours=1)).time(),
                activa=True
            )
            messages.success(request, f'¡Reserva confirmada! {recurso.identificador} está a tu nombre.')
    return redirect('lista_recursos')


'''
@login_required(login_url='/login/')
def liberar_recurso(request, recurso_id):
    if obtener_rol(request.user) not in ['Estudiante', 'Administrativo']:
        destino = redirigir_segun_rol(request.user)
        return destino if destino else redirect('login')
    if request.method == 'POST':
        recurso = get_object_or_404(RecursoFisico, id=recurso_id)
        recurso.estado = 'DISPONIBLE'
        recurso.save()
        messages.success(request, '{} vuelve a estar Disponible.'.format(recurso.identificador))
    return redirect('lista_recursos')
'''


@login_required(login_url='/login/')
def liberar_recurso(request, recurso_id):
    if obtener_rol(request.user) not in ['Estudiante', 'Administrativo']:
        return redirect('login')
    if request.method == 'POST':
        recurso = get_object_or_404(RecursoFisico, id=recurso_id)
        estudiante = obtener_o_crear_estudiante(request.user)
        if obtener_rol(request.user) == 'Estudiante':
            reserva = Reserva.objects.filter(sala=recurso, activa=True, estudiante=estudiante).first()
            if not reserva:
                messages.error(request, "No puedes liberar un equipo que tú no reservaste.")
                return redirect('lista_recursos')
            reserva.activa = False
            reserva.save()
        else:
            Reserva.objects.filter(sala=recurso, activa=True).update(activa=False)
        recurso.estado = 'DISPONIBLE'
        recurso.save()
        messages.success(request, f'{recurso.identificador} vuelve a estar Disponible.')
    return redirect('lista_recursos')


@login_required(login_url='/login/')
def lista_reportes(request):
    if obtener_rol(request.user) != 'Soporte TI':
        destino = redirigir_segun_rol(request.user)
        return destino if destino else redirect('login')
    reportes = ReporteIncidencia.objects.all()
    return render(request, 'lista_reportes.html', {'reportes': reportes})

'''
@login_required(login_url='/login/')
def crear_reporte(request):
    if obtener_rol(request.user) != 'Estudiante':
        destino = redirigir_segun_rol(request.user)
        return destino if destino else redirect('login')
    if request.method == 'POST':
        form = ReporteIncidenciaForm(request.POST)
        if form.is_valid():
            recurso_seleccionado = form.cleaned_data['recurso']
            if ReporteIncidencia.objects.filter(recurso=recurso_seleccionado, resuelto=False).exists():
                messages.error(request, "Este computador ({}) ya está reportado.".format(recurso_seleccionado.identificador))
                return render(request, 'crear_reporte.html', {'form': form})
            form.save()
            messages.success(request, "Reporte enviado correctamente.")
            return redirect('lista_recursos')
    else:
        form = ReporteIncidenciaForm()
    return render(request, 'crear_reporte.html', {'form': form})
'''

@login_required(login_url='/login/')
def crear_reporte(request):
    if obtener_rol(request.user) != 'Estudiante':
        return redirect('lista_recursos')
    if request.method == 'POST':
        form = ReporteIncidenciaForm(request.POST)
        if form.is_valid():
            reporte = form.save(commit=False)
            estudiante = Estudiante.objects.filter(user=request.user).first()
            if estudiante:
                reporte.estudiante = estudiante
                if ReporteIncidencia.objects.filter(recurso=reporte.recurso, resuelto=False).exists():
                    messages.error(request, f"Este computador ({reporte.recurso.identificador}) ya está reportado.")
                    return render(request, 'crear_reporte.html', {'form': form})
                reporte.save()
                messages.success(request, "Reporte enviado correctamente.")
                return redirect('lista_recursos')
            else:
                messages.error(request, "Error: No se encontró tu perfil de estudiante.")
    else:
        form = ReporteIncidenciaForm()
    return render(request, 'crear_reporte.html', {'form': form})


def poblar_bd(request):
    estudiantes = [
        {'rut': '21.111.111-1', 'nombre': 'Samy Contreras', 'carrera': 'Ingeniería en Informática'},
        {'rut': '22.222.222-2', 'nombre': 'Valentina Soto', 'carrera': 'Ingeniería en Informática'},
        {'rut': '23.333.333-3', 'nombre': 'Matías Torres', 'carrera': 'Analista Programador'},
        {'rut': '24.444.444-4', 'nombre': 'Camila Rojas', 'carrera': 'Administración de Empresas'},
        {'rut': '25.555.555-5', 'nombre': 'Diego Muñoz', 'carrera': 'Mecánica Automotriz'},
    ]
    for est in estudiantes:
        Estudiante.objects.get_or_create(rut=est['rut'], defaults=est)

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
        RecursoFisico.objects.get_or_create(identificador=rec['identificador'], defaults=rec)
        
    return HttpResponse("<h1>¡Éxito!</h1><p>Base de datos poblada en Supabase. Ya puedes volver a la página principal.</p>")




@login_required(login_url='/login/')
def lista_libros(request):
    libros = Libro.objects.all()
    return render(request, 'lista_libros.html', {'libros': libros})

def registro_estudiante(request):
    if request.method == 'POST':
        form = RegistroEstudianteForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Asignamos automáticamente el grupo de Estudiante
            grupo, _ = Group.objects.get_or_create(name='Estudiante')
            user.groups.add(grupo)
            messages.success(request, "Cuenta creada exitosamente. Ahora puedes iniciar sesión.")
            return redirect('login')
    else:
        form = RegistroEstudianteForm()
    return render(request, 'registro.html', {'form': form})

@login_required(login_url='/login/')
def crear_reserva(request):
    if obtener_rol(request.user) != 'Estudiante':
        return redirect('lista_recursos') 
    if request.method == 'POST':
        form = ReservaForm(request.POST)
        if form.is_valid():
            reserva = form.save(commit=False)
            try:
                estudiante = Estudiante.objects.get(user=request.user)
                reserva.estudiante = estudiante
                reserva.save()
                # Cambiamos el estado de la sala a OCUPADA automáticamente
                sala = reserva.sala
                sala.estado = 'OCUPADO'
                sala.save()
                messages.success(request, f"¡Sala {sala.identificador} reservada con éxito!")
                return redirect('lista_recursos')
            except Estudiante.DoesNotExist:
                messages.error(request, "Error: No tienes un perfil de estudiante asociado.")
    else:
        form = ReservaForm()
    return render(request, 'crear_reserva.html', {'form': form})

@login_required(login_url='/login/')
def crear_resena(request):
    libro_id = request.GET.get('libro')
    if request.method == 'POST':
        form = ResenaForm(request.POST)
        if form.is_valid():
            resena = form.save(commit=False)
            palabras_malas = ['tonto', 'estupido', 'basura', 'idiota', 'asqueroso']
            if any(palabra in resena.texto.lower() for palabra in palabras_malas):
                messages.error(request, "La reseña contiene lenguaje ofensivo. Por favor, sé respetuoso.")
                return render(request, 'crear_resena.html', {'form': form})
            estudiante = Estudiante.objects.filter(user=request.user).first()
            if estudiante:
                resena.estudiante = estudiante
                resena.save()
                messages.success(request, "Reseña publicada exitosamente.")
                return redirect('lista_libros')
    else:
        initial_data = {'libro': libro_id} if libro_id else {}
        form = ResenaForm(initial=initial_data)
    return render(request, 'crear_resena.html', {'form': form})

@login_required(login_url='/login/')
def eliminar_resena(request, resena_id):
    resena = get_object_or_404(Reseña, id=resena_id)
    
    # Validamos permisos: ¿Es admin? ¿O es el dueño de la reseña?
    es_admin = request.user.groups.filter(name='Administrativo').exists()
    es_dueno = (resena.estudiante.user == request.user)
    
    if es_admin or es_dueno:
        resena.delete()
        messages.success(request, "Reseña eliminada correctamente.")
    else:
        messages.error(request, "No tienes permiso para eliminar esta reseña.")
        
    return redirect('lista_libros')


