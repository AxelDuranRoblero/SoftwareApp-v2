# En SoftwareApp/SoftwareApp/urls.py

from django.contrib import admin
from django.urls import path
from ItemApp import views as item_views
from django.contrib.auth import views as auth_views # Lo dejamos para el logout

urlpatterns = [
    path('admin/', admin.site.urls),

    # ¡CORREGIDO!
    # La raíz ('') usa 'vista_inicio', que (gracias al paso 1)
    # ahora renderiza 'login.html' (la página NUAM).
    path('', item_views.vista_inicio, name='inicio'), 

    #
    # Borramos la URL '/login/' porque la página principal AHORA es el login.
    #

    # Mantenemos el logout (por si lo usas en el futuro)
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]