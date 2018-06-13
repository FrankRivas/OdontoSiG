from django.conf.urls import url
from  .views import *

urlpatterns = [
    url('^$', Inicio.as_view(), name='home'),
    url(r'^bitacora$', reporte_bitacora, name='reporte_bitacora'),
    url(r'^conexiones$', reporte_conexion, name='reporte_conexiones'),

#Reportes Tacticos
    url(r'^frecuencias_grupales', reporte_frec_grupales, name='frecuencias_grupales'),
    url(r'^prevalencia_piezas', reporte_comp_diagnostico, name='prevalencia_piezas'),
    url(r'^estado_superficie', reporte_est_superficie, name='estado_superficie'),
    url(r'^clasificacion_severidad', reporte_clas_severidad, name='clasificacion_severidad'),
    url(r'^clasificacion_paciente', reporte_clas_pacientes, name='clasificacion_pacientes'),
    url(r'^necesidad_segun_variable', reporte_nec_trat_svariable, name='necesidad_segun_variable'),

#Reportes Estrategicos
    url(r'^pacientes_atendidos', reporte_pac_atendidos, name='pacientes_atendidos'),
    url(r'^frecuencias', reporte_frecuencias, name='frecuencias'),
    url(r'^prevalencias', reporte_prevalencias, name='prevalencias'),
    url(r'^necesidades_tratamiento', reporte_nec_tratamiento, name='necesidades_tratamiento'),
    url(r'^severidad', reporte_severidad, name='severidad'),

    url('^pruebas/$', pruebas, name='Pruebas'),
    url('^pruebas/ajax/PruebaCreacion/$', prueba_creacion, name='PruebaCreacion'),
]