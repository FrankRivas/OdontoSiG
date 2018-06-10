from django.conf.urls import url
from  .views import *

urlpatterns = [
    url('^$', Inicio.as_view(), name='home'),
    url(r'^reportes/bitacora$', reporte_bitacora, name='reporte_bitacora'),
    url(r'^reportes/FrecuenciasGrupales', reporte_frec_grupales, name='FrecuenciasGrupales'),
    url(r'^reportes/ComparativoDiagnostico', reporte_comp_diagnostico, name='ComparativoDiagnostico'),
    url(r'^reportes/EstadoSuperficie', reporte_est_superficie, name='EstadoSuperficie'),
    url(r'^reportes/ClasificacionSeveridad', reporte_clas_severidad, name='ClasificacionSeveridad'),
    url(r'^reportes/ClasificacionPacientes', reporte_clas_pacientes, name='ClasificacionPacientes'),
    url(r'^reportes/conexiones$', reporte_conexion, name='reporte_conexiones'),
    url('^pruebas/$', pruebas, name='prueba'),
    url('^pruebas/ajax/prueba_creacion/$', prueba_creacion, name='prueba_creacion'),
]