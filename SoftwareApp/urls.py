from django.contrib import admin
from django.urls import path
from ItemApp import views as item_views

from django.contrib.auth import views as otras_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', item_views.vista_inicio, name='inicio'),
    path('login/', otras_views.LoginView.as_view(
        template_name='login.html' 
    ), name='login'),

    path('logout/', otras_views.LogoutView.as_view(), name='logout'),
]