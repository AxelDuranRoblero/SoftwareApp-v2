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
@login_required
def carga_datos(request):
    if request.method == 'POST':
        form = ArchivoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('carga_datos')
    else:
        form = ArchivoForm()

    archivos = Archivo.objects.all().order_by('-fecha_subida')
    return render(request, 'carga_datos.html', {'form': form, 'archivos': archivos})

@login_required
def vista_crear_calificacion(request):
    return render(request, 'crear_calificacion.html')

@login_required
def vista_reportes(request):
    return render(request, 'reportes.html')
