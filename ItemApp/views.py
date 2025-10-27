from django.shortcuts import render

# Tu vista de inicio (esta ya la tienes)
def vista_inicio(request):
    return render(request, 'inicio.html')

# 
# ¡AÑADE ESTA NUEVA VISTA!
# 
def vista_login_personalizado(request):
    # Ahora sí apunta al archivo 'login.html' (el de NUAM)
    return render(request, 'login.html')