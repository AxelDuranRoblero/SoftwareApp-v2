# En itemApp/views.py
from django.shortcuts import render

#
# ¡AQUÍ ESTÁ EL CAMBIO!
#
# La vista principal (para '/') ahora cargará tu página NUAM (login.html).
def vista_inicio(request):
    return render(request, 'login.html') 


# Esta función ('vista_login_personalizado') ahora es redundante
# porque 'vista_inicio' ya hace su trabajo.
def vista_login_personalizado(request):
    return render(request, 'login.html')