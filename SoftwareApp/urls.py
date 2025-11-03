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
    path('carga_datos/', item_views.carga_datos, name='carga_datos'),
    path('crear_calificacion/', item_views.vista_crear_calificacion, name='crear_calificacion'),
    path('reportes/', item_views.vista_reportes, name='reportes'),
]

from django.conf import settings
from django.conf.urls.static import static

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
