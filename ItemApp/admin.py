from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import CalificacionTributaria, AuditoriaCalificacion

@admin.register(CalificacionTributaria)
class CalificacionTributariaAdmin(admin.ModelAdmin):
    list_display = ['emisor', 'nemotecnico', 'pais', 'ano_tributario', 'monto_distribuido', 'corredor', 'usuario']
    list_filter = ['pais', 'tipo_instrumento', 'estado_inscripcion', 'ano_tributario', 'activo']
    search_fields = ['emisor', 'nemotecnico', 'rut_emisor', 'corredor']
    date_hierarchy = 'fecha_registro'
    ordering = ['-fecha_creacion']
    
    fieldsets = (
        ('Información del Emisor', {
            'fields': ('emisor', 'rut_emisor', 'pais')
        }),
        ('Información del Instrumento', {
            'fields': ('tipo_instrumento', 'nemotecnico', 'estado_inscripcion')
        }),
        ('Información Tributaria', {
            'fields': ('tipo_declaracion', 'ano_tributario', 'periodo')
        }),
        ('Montos y Factores', {
            'fields': ('monto_distribuido', 'factor_actualizacion', 'credito_fiscal', 'tasa_retencion', 'monto_actualizado', 'impuesto_calculado')
        }),
        ('Información del Corredor', {
            'fields': ('corredor', 'fecha_registro')
        }),
        ('Observaciones', {
            'fields': ('observaciones',)
        }),
        ('Metadata', {
            'fields': ('usuario', 'activo', 'fecha_creacion', 'fecha_modificacion'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['monto_actualizado', 'impuesto_calculado', 'fecha_creacion', 'fecha_modificacion']

@admin.register(AuditoriaCalificacion)
class AuditoriaCalificacionAdmin(admin.ModelAdmin):
    list_display = ['calificacion', 'usuario', 'accion', 'fecha_accion']
    list_filter = ['accion', 'fecha_accion']
    search_fields = ['calificacion__emisor', 'usuario__username']
    date_hierarchy = 'fecha_accion'
    ordering = ['-fecha_accion']
    readonly_fields = ['calificacion', 'usuario', 'accion', 'fecha_accion', 'datos_anteriores', 'datos_nuevos']