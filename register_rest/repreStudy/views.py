from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth import authenticate, login
from .models import Representante, Alumno
from .forms import RepresentanteForm, AlumnoForm, CustomUserCreationForm
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# para el login
def home(request):
    return render(request, './index.html')

# para el registro de usuario
def register(request):
    data = {
        'form': CustomUserCreationForm()
    }

    if request.method == 'POST':
        user_creation_form = CustomUserCreationForm(data=request.POST)

        if user_creation_form.is_valid():
            user_creation_form.save()

            user = authenticate(username=user_creation_form.cleaned_data['username'], password=user_creation_form.cleaned_data['password1'])
            login(request, user)
            return redirect('index')
        else:
            data['form'] = user_creation_form

    return render(request, 'registration/register.html', data)


@login_required
def representante_index(request, letter = None):
    # para buscar por la primera letra
    if letter != None:
        search_query = None
        representantes = Representante.objects.filter(nombres__istartswith=letter)
    else:
        # para el buscador
        search_query = request.GET.get('search', '')
        representantes = Representante.objects.filter(
            Q(nombres__icontains=search_query) |
            Q(apellidos__icontains=search_query) |
            Q(cedula__contains=search_query) |
            Q(serial_patria__contains=search_query) |
            Q(codigo_patria__contains=search_query)
        )

    # Verificar si no se encontraron representantes
    no_results_message = "No se encontraron coincidencias." if not representantes.exists() else None

    # Paginación
    paginator = Paginator(representantes, 7)  # Mostrar 8 representantes por página
    page_number = request.GET.get('page')  # Obtener el número de página de la solicitud
    try:
        page_obj = paginator.get_page(page_number)  # Obtener la página solicitada
    except PageNotAnInteger:
        page_obj = paginator.get_page(1)  # Si no es un número entero, mostrar la primera página
    except EmptyPage:
        page_obj = paginator.get_page(paginator.num_pages)  # Si está fuera del rango, mostrar la última página

    context = {
        'representantes': page_obj,  # Usar el objeto de la página en lugar de la lista completa
        'no_results_message': no_results_message,
        'search_query': search_query  # Pasar la consulta de búsqueda al contexto si existe
    }
    return render(request, 'representante/index.html', context)


# ver info representante
@login_required
def representante_view(request, id):
    representante = Representante.objects.get(id=id)
    alumnos = Alumno.objects.filter(representante=representante)
    context = {
        'representante': representante,
        'alumnos': alumnos
    }
    return render(request, 'representante/detail.html', context)

# para editar representante
@login_required
def representante_edit(request, id):
    contact = Representante.objects.get(id=id)

    # para que al darle al boton de editar nos muestre el formulario lleno y poder editarlo
    if request.method == 'GET':
        form = RepresentanteForm(instance=contact)
        context = {
            'form' : form,
            'id' : id
        }
        return render(request, 'representante/edit.html', context)

    # para que al editarlo y darle a guardar este guarde lo editado y sustituya al anterior
    if request.method == 'POST':
        form = RepresentanteForm(request.POST, instance=contact)
        if form.is_valid():
            form.save()
        context = {
            'form' : form,
            'id' : id
        }
        messages.success(request, "Representante actualizado.")
        return render(request, 'representante/edit.html', context)

# para añadir un representante nuevo
@login_required
def representante_create(request):
    # para darle al boton añadir y crear el formulario
    if request.method == 'GET':
        form = RepresentanteForm()
        context = {
            'form' : form
        }
        return render(request, 'representante/create.html', context)
    
    # para crear y guardar el nuevo contacto
    if request.method == 'POST':
        form = RepresentanteForm(request.POST)
        if form.is_valid():
            form.save()
        messages.success(request, "Representante añadido.")
        return redirect('representante_create')
    

# para eliminar un representante
@login_required
def representante_delete(request, id):
    return redirect('representante_confirm_delete', id=id)    

# para confirmar si desea eliminarlo
@login_required
def representante_confirm_delete(request, id):
    representante = get_object_or_404(Representante, id=id)
    if request.method == 'POST':
        representante.delete()
        messages.success(request, "Representante eliminado.")
        return redirect('representante')
    context = {
        'representante': representante
    }
    return render(request, 'representante/representante_confirm_delete.html', context)


################################################################################################

@login_required
def alumno_index(request, letter=None):
    if letter is not None:
        search_query = None
        alumnos = Alumno.objects.filter(nombres__istartswith=letter)
    else:
        search_query = request.GET.get('search', '')
        alumnos = Alumno.objects.filter(
            Q(nombres__icontains=search_query) |
            Q(apellidos__icontains=search_query) |
            Q(grado_y_seccion__icontains=search_query) |
            Q(sexo__icontains=search_query) |
            Q(edad__icontains=search_query)
        )

    no_results_message = "No se encontraron coincidencias." if not alumnos.exists() else None

    paginator = Paginator(alumnos, 8)
    page_number = request.GET.get('page')
    try:
        page_obj = paginator.get_page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.get_page(1)
    except EmptyPage:
        page_obj = paginator.get_page(paginator.num_pages)

    context = {
        'alumnos': page_obj,
        'no_results_message': no_results_message,
        'search_query': search_query
    }
    return render(request, 'alumno/index.html', context)


@login_required
def alumno_view(request, id):
    alumno = Alumno.objects.get(id=id)
    context = {
        'alumno': alumno
    }
    return render(request, 'alumno/detail.html', context)

def alumno_edit(request, id):
    alumno = Alumno.objects.get(id=id)

    if request.method == 'GET':
        form = AlumnoForm(instance=alumno)
        context = {
            'form': form,
            'id': id
        }
        return render(request, 'alumno/edit.html', context)

    if request.method == 'POST':
        form = AlumnoForm(request.POST, instance=alumno)
        if form.is_valid():
            form.save()
        context = {
            'form': form,
            'id': id
        }
        messages.success(request, "alumno actualizado.")
        return render(request, 'alumno/edit.html', context)


@login_required
def alumno_create(request):
    if request.method == 'GET':
        form = AlumnoForm()
        context = {
            'form': form
        }
        return render(request, 'alumno/create.html', context)

    if request.method == 'POST':
        form = AlumnoForm(request.POST)
        if form.is_valid():
            form.save()
        messages.success(request, "alumno añadido.")
        return redirect('alumno_create')


@login_required
def alumno_delete(request, id):
    return redirect('alumno_confirm_delete', id=id)


@login_required
def alumno_confirm_delete(request, id):
    alumno = get_object_or_404(Alumno, id=id)
    if request.method == 'POST':
        alumno.delete()
        messages.success(request, "alumno eliminado.")
        return redirect('alumno')
    context = {
        'alumno': alumno
    }
    return render(request, 'alumno/alumno_confirm_delete.html', context)
