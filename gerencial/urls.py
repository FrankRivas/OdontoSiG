from django.conf.urls import url
from  .views import *

urlpatterns = [
    url('^$', Inicio.as_view(), name='home'),
    url(r'^reportes/bitacora$', reporte_bitacora, name='reporte_bitacora'),
    url(r'^reportes/conexiones$', reporte_conexion, name='reporte_conexiones'),
    url('^pruebas/$', pruebas, name='prueba'),
    url('^pruebas/ajax/prueba_creacion/$', prueba_creacion, name='prueba_creacion'),
]