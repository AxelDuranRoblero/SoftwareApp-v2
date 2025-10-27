from django.shortcuts import render

#
# ¡IMPORTANTE!
# Tu vista 'vista_inicio' ahora la llamaremos 'vista_registro'
# porque es la página de registro de NUAM (login.html).
#
def vista_registro(request):
    # Esta sigue siendo tu página NUAM (login.html)
    return render(request, 'login.html') 

#
# ¡NUEVA VISTA!
# Esta será la nueva página principal (la portada)
#
def vista_antepagina(request):
    return render(request, 'antepagina.html')

#
# ¡NUEVA VISTA!
# Esta es la página que ve el usuario DESPUÉS de iniciar sesión
#
def vista_inicio_logueado(request):
    return render(request, 'inicio.html')