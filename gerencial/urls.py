from django.conf.urls import url
from  .views import *

urlpatterns = [
    url('^$', Inicio.as_view(), name='home'),
]