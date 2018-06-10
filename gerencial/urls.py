from django.conf.urls import url
from  .views import *

urlpatterns = [
    url('^$', Inicio.as_view(), name='home'),
    url(r'^reportes/bitacora$', reporte_bitacora, name='reporte_bitacora'),
    url(r'^reportes/conexiones$', reporte_conexion, name='reporte_conexiones'),

#Reportes Tacticos
    url(r'^reportes/FrecuenciasGrupales', reporte_frec_grupales, name='FrecuenciasGrupales'),
    url(r'^reportes/ComparativoDiagnostico', reporte_comp_diagnostico, name='ComparativoDiagnostico'),
    url(r'^reportes/EstadoSuperficie', reporte_est_superficie, name='EstadoSuperficie'),
    url(r'^reportes/ClasificacionSeveridad', reporte_clas_severidad, name='ClasificacionSeveridad'),
    url(r'^reportes/ClasificacionPacientes', reporte_clas_pacientes, name='ClasificacionPacientes'),
    url(r'^reportes/NecesidadesSegunVariables', reporte_nec_trat_svariable, name='NecesidadesSegunVariables'),

#Reportes Estrategicos
    url(r'^reportes/PacientesAtendidos', reporte_pac_atendidos, name='PacientesAtendidos'),
    url(r'^reportes/Frecuencias', reporte_frecuencias, name='Frecuencias'),
    url(r'^reportes/Prevalencias', reporte_prevalencias, name='Prevalencias'),
    url(r'^reportes/NecesidadesTratamiento', reporte_nec_tratamiento, name='NecesidadesTratamiento'),
    url(r'^reportes/Severidad', reporte_severidad, name='Severidad'),

    url('^pruebas/$', pruebas, name='prueba'),
    url('^pruebas/ajax/prueba_creacion/$', prueba_creacion, name='prueba_creacion'),
]