from django.contrib import admin
from django.urls import path
from ItemApp import views as item_views # 
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('', item_views.vista_inicio, name='inicio'),

    path('login/', item_views.vista_login_personalizado, name='login'),

    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]