from django.shortcuts import render
from django.contrib.auth import logout
from django.shortcuts import redirect


def vista_registro(request):

    return render(request, 'login.html') 


def vista_antepagina(request):
    return render(request, 'antepagina.html')


def vista_inicio_logueado(request):
    return render(request, 'inicio.html')