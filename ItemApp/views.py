from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from .models import CalificacionTributaria, AuditoriaCalificacion
from datetime import datetime


def vista_registro(request):

    return render(request, 'login.html') 


def vista_antepagina(request):
    return render(request, 'antepagina.html')


def vista_inicio_logueado(request):
    return render(request, 'inicio.html')


import json

@login_required
def inicio(request):
    """Vista del dashboard principal con estadísticas"""

    total_calificaciones = CalificacionTributaria.objects.filter(usuario=request.user, activo=True).count()
    

    ultimas_calificaciones = CalificacionTributaria.objects.filter(
        usuario=request.user, 
        activo=True
    ).order_by('-fecha_creacion')[:5]
    

    stats_por_pais = CalificacionTributaria.objects.filter(
        usuario=request.user, 
        activo=True
    ).values('pais').annotate(total=models.Count('id'))
    
    context = {
        'total_calificaciones': total_calificaciones,
        'ultimas_calificaciones': ultimas_calificaciones,
        'stats_por_pais': stats_por_pais,
    }
    
    return render(request, 'inicio.html', context)

@login_required
def crear_calificacion(request):
    """Vista para crear una nueva calificación tributaria"""
    if request.method == 'POST':
        try:

            calificacion = CalificacionTributaria(

                emisor=request.POST.get('emisor'),
                rut_emisor=request.POST.get('rut_emisor'),
                pais=request.POST.get('pais'),
                
                
                tipo_instrumento=request.POST.get('tipo_instrumento'),
                nemotecnico=request.POST.get('nemotecnico').upper(),
                estado_inscripcion=request.POST.get('estado_inscripcion'),
                
   
                tipo_declaracion=request.POST.get('tipo_declaracion'),
                ano_tributario=request.POST.get('ano_tributario'),
                periodo=request.POST.get('periodo'),
                
        
                monto_distribuido=request.POST.get('monto_distribuido'),
                factor_actualizacion=request.POST.get('factor_actualizacion') or 1.0000,
                credito_fiscal=request.POST.get('credito_fiscal') or None,
                tasa_retencion=request.POST.get('tasa_retencion') or None,
                

                corredor=request.POST.get('corredor'),
                fecha_registro=request.POST.get('fecha_registro'),
                

                observaciones=request.POST.get('observaciones'),
                

                usuario=request.user
            )
            
        
            calificacion.save()
            

            AuditoriaCalificacion.objects.create(
                calificacion=calificacion,
                usuario=request.user,
                accion='crear',
                datos_nuevos={
                    'emisor': calificacion.emisor,
                    'nemotecnico': calificacion.nemotecnico,
                    'monto_distribuido': str(calificacion.monto_distribuido),
                }
            )
            
            messages.success(request, f'✅ Calificación tributaria creada exitosamente para {calificacion.emisor}')
            return redirect('listar_calificaciones')
            
        except Exception as e:
            messages.error(request, f'❌ Error al crear la calificación: {str(e)}')
    
    return render(request, 'crear_calificacion.html')

@login_required
def listar_calificaciones(request):
    """Vista para listar todas las calificaciones con filtros"""
    calificaciones = CalificacionTributaria.objects.filter(usuario=request.user, activo=True)
    
    pais = request.GET.get('pais')
    ano = request.GET.get('ano')
    tipo_instrumento = request.GET.get('tipo_instrumento')
    emisor = request.GET.get('emisor')
    
    if pais:
        calificaciones = calificaciones.filter(pais=pais)
    if ano:
        calificaciones = calificaciones.filter(ano_tributario=ano)
    if tipo_instrumento:
        calificaciones = calificaciones.filter(tipo_instrumento=tipo_instrumento)
    if emisor:
        calificaciones = calificaciones.filter(emisor__icontains=emisor)
    
    paginator = Paginator(calificaciones, 20) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'total': calificaciones.count(),
        'filtros': {
            'pais': pais,
            'ano': ano,
            'tipo_instrumento': tipo_instrumento,
            'emisor': emisor,
        }
    }
    
    return render(request, 'listar_calificaciones.html', context)

@login_required
def modificar_calificacion(request, id):
    """Vista para modificar una calificación existente"""
    calificacion = get_object_or_404(CalificacionTributaria, id=id, usuario=request.user)
    
    if request.method == 'POST':
        try:
            datos_anteriores = {
                'monto_distribuido': str(calificacion.monto_distribuido),
                'factor_actualizacion': str(calificacion.factor_actualizacion),
            }
            
            calificacion.emisor = request.POST.get('emisor')
            calificacion.rut_emisor = request.POST.get('rut_emisor')
            
            calificacion.save()
            

            AuditoriaCalificacion.objects.create(
                calificacion=calificacion,
                usuario=request.user,
                accion='modificar',
                datos_anteriores=datos_anteriores,
                datos_nuevos={'monto_distribuido': str(calificacion.monto_distribuido)}
            )
            
            messages.success(request, '✅ Calificación modificada exitosamente')
            return redirect('listar_calificaciones')
            
        except Exception as e:
            messages.error(request, f'❌ Error al modificar: {str(e)}')
    
    return render(request, 'modificar_calificacion.html', {'calificacion': calificacion})

@login_required
def eliminar_calificacion(request, id):
    """Vista para eliminar (desactivar) una calificación"""
    calificacion = get_object_or_404(CalificacionTributaria, id=id, usuario=request.user)
    
    if request.method == 'POST':
        calificacion.activo = False
        calificacion.save()
        

        AuditoriaCalificacion.objects.create(
            calificacion=calificacion,
            usuario=request.user,
            accion='eliminar'
        )
        
        messages.success(request, '✅ Calificación eliminada exitosamente')
        return redirect('listar_calificaciones')
    
    return render(request, 'eliminar_calificacion.html', {'calificacion': calificacion})
