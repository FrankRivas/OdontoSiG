from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.http import HttpResponse
import json
from django.contrib.staticfiles.templatetags.staticfiles import static
from django import forms
import base64
from .forms import *
from decimal import Decimal

from gerencial.models import Bitacora, Accion
from django.contrib.auth.models import User
import locale
import datetime
from datetime import timedelta
from operator import itemgetter
from operator import itemgetter
# Create your views here.
class Inicio(LoginRequiredMixin, TemplateView):
    template_name = "base.html"

def reporte_bitacora(request):
    locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
    if request.method == 'POST':
        g = False
        if request.POST.get('fecha_desde'):
            desde = datetime.datetime.strptime(request.POST.get('fecha_desde'), '%d/%m/%Y').strftime("%d de %B de %Y")
        else:
            desde = "el origen de los tiempos"
        fecha_hasta = request.POST.get('fecha_hasta')
    else:
        g = True
        fecha_desde = (datetime.date.today() - timedelta(datetime.date.today().day - 1)).strftime("%Y-%m-%d")
        desde = (datetime.date.today() - timedelta(datetime.date.today().day - 1)).strftime("%d de %B de %Y")
    try:
        hasta = datetime.datetime.strptime(fecha_hasta, '%d/%m/%Y').strftime("%d de %B de %Y")
    except:
        hasta = datetime.date.today().strftime("%d de %B de %Y")

    # Filtrando las Citas Médicas
    acciones = Bitacora.objects.all()
    if g:
        acciones = acciones.filter(FechaAccion__gte=fecha_desde)
    if request.POST.get('fecha_desde'):
        a = request.POST.get('fecha_desde')
        acciones = acciones.filter(FechaAccion__gte=a[6:] + "-" + a[3:5] + "-" + a[:2])
    if request.POST.get('fecha_hasta'):
        b = request.POST.get('fecha_hasta')
        acciones = acciones.filter(FechaAccion__lte=b[6:] + "-" + b[3:5] + "-" + b[:2])

    #acciones = Bitacora.objects.all()

    context = {
        'acciones': acciones,

    }

    return render(request, 'reporte_bitacora.html', context)


def reporte_conexion(request):
    conexiones = User.objects.all()

    context = {
        'conexiones': conexiones,
    }

    return render(request, 'reporte_conexiones.html', context)

#Highchars
def pruebas(self):
    return render(self, 'pruebas.html')

def prueba_creacion(request):
    #La imagen de logo la envío en base64
    img = "static/gerencial/img/odonto_logo.png"
    with open(img, 'rb') as f:
        contents = f.read()
        base = base64.b64encode(contents)
        image = "data:image/png;base64," + base.decode('utf-8')

    chart = {
        "chart":{
            #Tipo de gráfico y espacio de header
            "type":"pie",
            "spacingTop": 200
        },
        #Mantiene el formato de html en la exportación
        "exporting":{
            "enabled":"true",
            "allowHTML":"true",
            "buttons": {
                "contextButton": {
                    "menuItems": [ "downloadPNG", "downloadPDF", "downloadJPEG"]
                }
            }
        },
        "plotOptions":{
            #Tamaño del diámetro del gráfico
            "pie": {
                "size":250
            },
            #Opciones de labels en el gráfico
            "series": {
                "dataLabels":{
                    "align":"left",
                    "enabled":"true"
                }
            }
        },
        "legend":{
            "enabled":"true",
            "align":"center"
        },
        #Información en base a la que se construye el gráfico
        "series": [{
            "showInLegend":"true",
            "name": "Parámetro de dato",
            "data":[
                {"name":"Primero","y":25.5},
                {"name":"Segundo","y":25.5},
                {"name":"Tercero","y":49.0}
            ]
        }]
    }
    #Para variables extras se utiliza esta coleccion
    #Agregar titulo y texto del período
    render = {
        "dataLabelFunction":"return this.point.name+':'+this.percentage.toFixed(1)+'%'",
        "image": image,
        "titulo": "Este es un título demasiado largo como para estar en una sola línea",
        "periodo":"Datos recolectados del dd/mm/aaaa al dd/mm/aaaa"
    }
    return JsonResponse({"chart": chart,"render": render})
#Fin highcharts