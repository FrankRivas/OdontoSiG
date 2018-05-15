from django.conf.urls import url
from django.contrib.auth.views import password_reset, password_reset_done, password_reset_confirm, password_reset_complete
from .views import *

urlpatterns = [
    url(r'^login/$', login, name='login'),
    url(r'^logout/$', logout, name='logout'),
    url(r'^cuenta/$', cuenta, name='cuenta'),

    # Inician urls para Usuario
    url(r'^agregar_usuario/', agregar_usuario, name='agregar_usuario'),
    url(r'^usuarios/$', usuarios, name='usuarios'),
    url(r'^actualizar_usuario/(?P<pk>\d+)$', ActualizarUsuario.as_view(), name='actualizar_usuario'),
    url(r'^eliminar_usuario/(?P<pk>\d+)$', eliminar_usuario, name='eliminar_usuario'),
    url(r'^bloquear_usuario/(?P<pk>\d+)$', bloquear_usuario, name='bloquear_usuario'),
    # Finalizan urls para Usuario

    url(r'^restablecer-contraseña/$', password_reset, {'post_reset_redirect': 'restablecer_contraseña_hecho'}, name='restablecer-contraseña'),
    url(r'^restablecer-contraseña/hecho/$', password_reset_done, name='restablecer_contraseña_hecho'),
    url(r'^restablecer-contraseña/confirmar/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', password_reset_confirm, {'post_reset_redirect': 'restablecer_contraseña_completado'}, name='restablecer_contraseña_confirmar'),
    url(r'^restablecer-contraseña/completado/$', password_reset_complete, name='restablecer_contraseña_completado')
]