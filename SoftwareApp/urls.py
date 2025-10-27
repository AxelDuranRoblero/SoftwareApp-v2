from django.contrib import admin
from django.urls import path
from ItemApp import views as item_views
from django.contrib.auth import views as vistas

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', item_views.vista_antepagina, name='antepagina'),
    path('registro/', item_views.vista_registro, name='registro'),
    path('login/', vistas.LoginView.as_view(
        template_name='login_tradicional.html'
    ), name='login'),
    path('inicio/', item_views.vista_inicio_logueado, name='inicio'),
    path('logout/', vistas.LogoutView.as_view(), name='logout'),
]