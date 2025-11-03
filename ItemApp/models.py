from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal
# Create your models here.


class CalificacionTributaria(models.Model):
    TIPO_INSTRUMENTO_CHOICES = [
        ('accion', 'Acción'),
        ('bono', 'Bono'),
        ('derivado', 'Derivado'),
        ('fondo_mutuo', 'Fondo Mutuo'),
        ('etf', 'ETF'),
    ]
    
    PAIS_CHOICES = [
        ('chile', 'Chile'),
        ('colombia', 'Colombia'),
        ('peru', 'Perú'),
    ]
    
    ESTADO_INSCRIPCION_CHOICES = [
        ('inscrito', 'Inscrito'),
        ('no_inscrito', 'No Inscrito'),
    ]
    
    TIPO_DECLARACION_CHOICES = [
        ('dj1948', 'DJ1948 - Dividendos'),
        ('dj1847', 'DJ1847 - Intereses'),
        ('certificado', 'Certificado Emisor'),
    ]
    
    PERIODO_CHOICES = [
        ('anual', 'Anual'),
        ('semestral', 'Semestral'),
        ('trimestral', 'Trimestral'),
    ]
    

    emisor = models.CharField(max_length=200, verbose_name="Nombre del Emisor")
    rut_emisor = models.CharField(max_length=12, verbose_name="RUT Emisor")
    pais = models.CharField(max_length=20, choices=PAIS_CHOICES, verbose_name="País")
    

    tipo_instrumento = models.CharField(max_length=50, choices=TIPO_INSTRUMENTO_CHOICES, verbose_name="Tipo de Instrumento")
    nemotecnico = models.CharField(max_length=20, verbose_name="Nemotécnico")
    estado_inscripcion = models.CharField(max_length=20, choices=ESTADO_INSCRIPCION_CHOICES, verbose_name="Estado de Inscripción")
    

    tipo_declaracion = models.CharField(max_length=50, choices=TIPO_DECLARACION_CHOICES, verbose_name="Tipo de Declaración")
    ano_tributario = models.IntegerField(verbose_name="Año Tributario", validators=[MinValueValidator(2020), MaxValueValidator(2030)])
    periodo = models.CharField(max_length=20, choices=PERIODO_CHOICES, verbose_name="Período")
    

    monto_distribuido = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="Monto Distribuido")
    factor_actualizacion = models.DecimalField(max_digits=10, decimal_places=4, blank=True, null=True, default=1.0000, verbose_name="Factor de Actualización")
    credito_fiscal = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, verbose_name="Crédito Fiscal (%)")
    tasa_retencion = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, verbose_name="Tasa de Retención (%)")
    monto_actualizado = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True, verbose_name="Monto Actualizado")
    impuesto_calculado = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True, verbose_name="Impuesto Calculado")
    

    corredor = models.CharField(max_length=200, verbose_name="Corredor de Bolsa")
    fecha_registro = models.DateField(verbose_name="Fecha de Registro")
    

    observaciones = models.TextField(blank=True, null=True, verbose_name="Observaciones")
    

    usuario = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Usuario", related_name='calificaciones')
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")
    fecha_modificacion = models.DateTimeField(auto_now=True, verbose_name="Última Modificación")
    activo = models.BooleanField(default=True, verbose_name="Activo")
    
    class Meta:
        verbose_name = "Calificación Tributaria"
        verbose_name_plural = "Calificaciones Tributarias"
        ordering = ['-ano_tributario', '-fecha_creacion']
        indexes = [
            models.Index(fields=['emisor', 'ano_tributario']),
            models.Index(fields=['nemotecnico']),
            models.Index(fields=['corredor', 'fecha_registro']),
        ]
    
    def __str__(self):
        return f"{self.emisor} - {self.nemotecnico} - {self.ano_tributario}"
    
    def save(self, *args, **kwargs):

        if self.monto_distribuido:
            factor = self.factor_actualizacion or Decimal('1.0000')
            self.monto_actualizado = self.monto_distribuido * factor
            
            if self.tasa_retencion:
                self.impuesto_calculado = self.monto_actualizado * (self.tasa_retencion / Decimal('100'))
        
        super().save(*args, **kwargs)



class AuditoriaCalificacion(models.Model):
    ACCION_CHOICES = [
        ('crear', 'Crear'),
        ('modificar', 'Modificar'),
        ('eliminar', 'Eliminar'),
    ]
    
    calificacion = models.ForeignKey(CalificacionTributaria, on_delete=models.CASCADE, related_name='auditorias')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    accion = models.CharField(max_length=20, choices=ACCION_CHOICES)
    fecha_accion = models.DateTimeField(auto_now_add=True)
    datos_anteriores = models.JSONField(blank=True, null=True)
    datos_nuevos = models.JSONField(blank=True, null=True)
    
    class Meta:
        verbose_name = "Auditoría"
        verbose_name_plural = "Auditorías"
        ordering = ['-fecha_accion']
    
    def __str__(self):
        return f"{self.accion} - {self.calificacion} - {self.fecha_accion}"



