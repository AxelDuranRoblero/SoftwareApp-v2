from django.contrib import admin
from django.urls import path
from ItemApp import views as item_views
from django.contrib.auth import views as auth_views # Para el login y logout

urlpatterns = [
    path('admin/', admin.site.urls),

    # 1. Portada (la nueva página principal '/')
    # Apunta a 'vista_antepagina'
    path('', item_views.vista_antepagina, name='antepagina'),
    
    # 2. Página de Registro NUAM ('/registro/')
    # Apunta a 'vista_registro' (que carga login.html)
    path('registro/', item_views.vista_registro, name='registro'),
    
    # 3. Página de Login Tradicional ('/login/')
    # Usa la vista de Django pero con nuestra nueva plantilla
    path('login/', auth_views.LoginView.as_view(
        template_name='login_tradicional.html'
    ), name='login'),
    
    # 4. Página de Inicio Post-Login ('/inicio/')
    # Apunta a 'vista_inicio_logueado'
    path('inicio/', item_views.vista_inicio_logueado, name='inicio'),

    # 5. Logout (se queda igual)
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]