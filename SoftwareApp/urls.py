

from django.contrib import admin
from django.urls import path

from ItemApp import views as item_views 

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('', item_views.vista_inicio, name='inicio'),
]