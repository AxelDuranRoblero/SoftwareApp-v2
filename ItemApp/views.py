from django.shortcuts import render
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from .models import Archivo
from .forms import ArchivoForm

def vista_registro(request):

    return render(request, 'login.html') 


def vista_antepagina(request):
    return render(request, 'antepagina.html')


def vista_inicio_logueado(request):
    return render(request, 'inicio.html')

@login_required
def vista_carga_datos(request):
    archivos = Archivo.objects.filter(usuario=request.user).order_by('-fecha_subida') # type: ignore
    if request.method == 'POST':
        form = ArchivoForm(request.POST, request.FILES)
        if form.is_valid():
            archivo = form.save(commit=False)
            archivo.usuario = request.user
            archivo.save()
            return redirect('carga_datos')
    else:
        form = ArchivoForm()
    return render(request, 'carga_datos.html', {'form': form, 'archivos': archivos})

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def vista_crear_calificacion(request):
    return render(request, 'crear_calificacion.html')
