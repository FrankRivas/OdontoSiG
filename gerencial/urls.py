from django.conf.urls import url
from  .views import *

urlpatterns = [
    url('^$', Inicio.as_view(), name='home'),
    url('^pruebas/$', pruebas, name='prueba'),
    url('^pruebas/ajax/prueba_creacion/$', prueba_creacion, name='prueba_creacion'),
]
