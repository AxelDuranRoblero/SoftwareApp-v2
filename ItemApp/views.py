from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Count
from .models import CalificacionTributaria, AuditoriaCalificacion


# Vistas existentes
def vista_registro(request):
    return render(request, 'login.html') 


def vista_antepagina(request):
    return render(request, 'antepagina.html')


@login_required
def vista_inicio_logueado(request):
    """Dashboard principal con estadísticas"""
    # Obtener estadísticas para el dashboard
    total_calificaciones = CalificacionTributaria.objects.filter(
        usuario=request.user, 
        activo=True
    ).count()
    
    # Últimas calificaciones creadas
    ultimas_calificaciones = CalificacionTributaria.objects.filter(
        usuario=request.user, 
        activo=True
    ).order_by('-fecha_creacion')[:5]
    
    # Estadísticas por país
    stats_por_pais = CalificacionTributaria.objects.filter(
        usuario=request.user, 
        activo=True
    ).values('pais').annotate(total=Count('id'))
    
    context = {
        'total_calificaciones': total_calificaciones,
        'ultimas_calificaciones': ultimas_calificaciones,
        'stats_por_pais': stats_por_pais,
    }
    
    return render(request, 'inicio.html', context)


# Nuevas vistas para calificaciones tributarias
@login_required
def vista_crear_calificacion(request):
    """Vista para crear una nueva calificación tributaria"""
    if request.method == 'POST':
        try:
            # Crear nueva calificación
            calificacion = CalificacionTributaria(
                # Información del Emisor
                emisor=request.POST.get('emisor'),
                rut_emisor=request.POST.get('rut_emisor'),
                pais=request.POST.get('pais'),
                
                # Información del Instrumento
                tipo_instrumento=request.POST.get('tipo_instrumento'),
                nemotecnico=request.POST.get('nemotecnico').upper(),
                estado_inscripcion=request.POST.get('estado_inscripcion'),
                
                # Información Tributaria
                tipo_declaracion=request.POST.get('tipo_declaracion'),
                ano_tributario=request.POST.get('ano_tributario'),
                periodo=request.POST.get('periodo'),
                
                # Montos y Factores
                monto_distribuido=request.POST.get('monto_distribuido'),
                factor_actualizacion=request.POST.get('factor_actualizacion') or 1.0000,
                credito_fiscal=request.POST.get('credito_fiscal') or None,
                tasa_retencion=request.POST.get('tasa_retencion') or None,
                
                # Información del Corredor
                corredor=request.POST.get('corredor'),
                fecha_registro=request.POST.get('fecha_registro'),
                
                # Observaciones
                observaciones=request.POST.get('observaciones'),
                
                # Usuario
                usuario=request.user
            )
            
            # Guardar (los cálculos se hacen automáticamente en el modelo)
            calificacion.save()
            
            # Crear registro de auditoría
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
def vista_listar_calificaciones(request):
    """Vista para listar todas las calificaciones con filtros"""
    calificaciones = CalificacionTributaria.objects.filter(
        usuario=request.user, 
        activo=True
    )
    
    # Aplicar filtros desde GET
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
    
    # Paginación
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
def vista_modificar_calificacion(request, id):
    """Vista para modificar una calificación existente"""
    calificacion = get_object_or_404(
        CalificacionTributaria, 
        id=id, 
        usuario=request.user
    )
    
    if request.method == 'POST':
        try:
            # Guardar datos anteriores para auditoría
            datos_anteriores = {
                'emisor': calificacion.emisor,
                'monto_distribuido': str(calificacion.monto_distribuido),
                'factor_actualizacion': str(calificacion.factor_actualizacion),
            }
            
            # Actualizar campos
            calificacion.emisor = request.POST.get('emisor')
            calificacion.rut_emisor = request.POST.get('rut_emisor')
            calificacion.pais = request.POST.get('pais')
            calificacion.tipo_instrumento = request.POST.get('tipo_instrumento')
            calificacion.nemotecnico = request.POST.get('nemotecnico').upper()
            calificacion.estado_inscripcion = request.POST.get('estado_inscripcion')
            calificacion.tipo_declaracion = request.POST.get('tipo_declaracion')
            calificacion.ano_tributario = request.POST.get('ano_tributario')
            calificacion.periodo = request.POST.get('periodo')
            calificacion.monto_distribuido = request.POST.get('monto_distribuido')
            calificacion.factor_actualizacion = request.POST.get('factor_actualizacion') or 1.0000
            calificacion.credito_fiscal = request.POST.get('credito_fiscal') or None
            calificacion.tasa_retencion = request.POST.get('tasa_retencion') or None
            calificacion.corredor = request.POST.get('corredor')
            calificacion.fecha_registro = request.POST.get('fecha_registro')
            calificacion.observaciones = request.POST.get('observaciones')
            
            calificacion.save()
            
            # Crear registro de auditoría
            datos_nuevos = {
                'emisor': calificacion.emisor,
                'monto_distribuido': str(calificacion.monto_distribuido),
                'factor_actualizacion': str(calificacion.factor_actualizacion),
            }
            
            AuditoriaCalificacion.objects.create(
                calificacion=calificacion,
                usuario=request.user,
                accion='modificar',
                datos_anteriores=datos_anteriores,
                datos_nuevos=datos_nuevos
            )
            
            messages.success(request, '✅ Calificación modificada exitosamente')
            return redirect('listar_calificaciones')
            
        except Exception as e:
            messages.error(request, f'❌ Error al modificar: {str(e)}')
    
    context = {
        'calificacion': calificacion
    }
    
    return render(request, 'modificar_calificacion.html', context)


@login_required
def vista_eliminar_calificacion(request, id):
    """Vista para eliminar (desactivar) una calificación"""
    calificacion = get_object_or_404(
        CalificacionTributaria, 
        id=id, 
        usuario=request.user
    )
    
    if request.method == 'POST':
        # No eliminar físicamente, solo desactivar (soft delete)
        calificacion.activo = False
        calificacion.save()
        
        # Crear registro de auditoría
        AuditoriaCalificacion.objects.create(
            calificacion=calificacion,
            usuario=request.user,
            accion='eliminar',
            datos_anteriores={
                'emisor': calificacion.emisor,
                'nemotecnico': calificacion.nemotecnico,
            }
        )
        
        messages.success(request, '✅ Calificación eliminada exitosamente')
        return redirect('listar_calificaciones')
    
    context = {
        'calificacion': calificacion
    }
    
    return render(request, 'eliminar_calificacion.html', context)


@login_required
def vista_detalle_calificacion(request, id):
    """Vista para ver el detalle completo de una calificación"""
    calificacion = get_object_or_404(
        CalificacionTributaria, 
        id=id, 
        usuario=request.user
    )
    
    # Obtener historial de auditoría
    auditorias = AuditoriaCalificacion.objects.filter(
        calificacion=calificacion
    ).order_by('-fecha_accion')
    
    context = {
        'calificacion': calificacion,
        'auditorias': auditorias,
    }
    
    return render(request, 'detalle_calificacion.html', context)


@login_required
def vista_carga_datos(request):
    """Vista para carga masiva de datos (futura implementación)"""
    # Esta vista será para cargar archivos Excel/CSV masivamente
    return render(request, 'carga_datos.html')


@login_required
def vista_reportes(request):
    """Vista para generar reportes"""
    # Obtener datos para reportes
    calificaciones = CalificacionTributaria.objects.filter(
        usuario=request.user,
        activo=True
    )
    
    # Estadísticas generales
    total_monto = sum([c.monto_distribuido for c in calificaciones])
    total_impuestos = sum([c.impuesto_calculado or 0 for c in calificaciones])
    
    # Agrupaciones
    por_pais = calificaciones.values('pais').annotate(
        total=Count('id'),
        monto_total=models.Sum('monto_distribuido')
    )
    
    por_ano = calificaciones.values('ano_tributario').annotate(
        total=Count('id'),
        monto_total=models.Sum('monto_distribuido')
    ).order_by('-ano_tributario')
    
    context = {
        'total_calificaciones': calificaciones.count(),
        'total_monto': total_monto,
        'total_impuestos': total_impuestos,
        'por_pais': por_pais,
        'por_ano': por_ano,
    }
    
    return render(request, 'reportes.html', context)

