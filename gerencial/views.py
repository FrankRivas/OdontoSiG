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
from django.db import connection
from gerencial.models import Bitacora, Accion, Paciente
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

#Inicia reporte de frecuencias grupales

def reporte_frec_grupales(request):

    if request.method=='POST':
        fecha_inicio = request.POST.get('fecha_desde')
        fecha_final = request.POST.get('fecha_hasta')
        criterio = request.POST.get('criterio')
        cod_criterio = '"EstICDAS"'
        if criterio == '1':
            cod_criterio = '"EstOMS"'
        context = consultar_indices(cod_criterio, fecha_inicio, fecha_final)
    else: #Desde el principio de los tiempos
        context = consultar_indices('"EstICDAS"', '1999-01-01', datetime.date.today())

    return render(request, 'reporte_frec_grupales.html', context)

def consultar_indices(criterio, fecha_inicial, fecha_final):
    context = {}
    indices = ['cpod', 'ceod', 'cpom', 'cpos']
    cpod_query = 'select ' + criterio + ' as Estado, count(*) as Cantidad from gerencial_paciente as a join gerencial_pieza as b on a.id=b."Paciente_id" where "Posicion"<47 and (a."FechaConsul" > %s and a."FechaConsul" < %s) group by ' + criterio + ' order by array_position(array[%s::char, %s::char, %s::char, %s::char], ' + criterio + '::char);'
    ceod_query = 'select ' + criterio + ' as Estado, count(*) as Cantidad from gerencial_paciente as a join gerencial_pieza as b on a.id=b."Paciente_id" where "Posicion">51 and (a."FechaConsul" > %s and a."FechaConsul" < %s) group by ' + criterio + ' order by array_position(array[%s::char, %s::char, %s::char, %s::char], ' + criterio + '::char);'
    cpom_query = 'select ' + criterio + ' as Estado, count(*) as Cantidad from gerencial_paciente as a join gerencial_pieza as b on a.id=b."Paciente_id" where ("Posicion"=16 or "Posicion"=26 or "Posicion"=36 or "Posicion"=46) and (a."FechaConsul" > %s and a."FechaConsul" < %s) group by ' + criterio + ' order by array_position(array[%s::char, %s::char, %s::char, %s::char], ' + criterio + '::char);'
    cpos_query = 'select ' + criterio + ' as Estado, count(*) as Cantidad from gerencial_paciente as a join gerencial_superficie as b on a.id=b."Paciente_id" where (a."FechaConsul" > %s and a."FechaConsul" < %s) group by ' + criterio + ' order by array_position(array[%s::char, %s::char, %s::char, %s::char], ' + criterio + '::char);'
    queries = [cpod_query, ceod_query, cpom_query, cpos_query]

    with connection.cursor() as cursor:
        i = 0
        for ind in indices:
            cursor.execute(queries[i], [fecha_inicial, fecha_final, 'Cariado', 'Perdido', 'Obturado', 'Sano'])
            context[ind] = procesar_resultado_frecuencias(cursor)
            i = i + 1

    return context


def procesar_resultado_frecuencias(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    query_dict = [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

    total_pacientes = Paciente.objects.count()
    for q in query_dict:
        q['frecuencia'] = q.get('cantidad')/total_pacientes

    return query_dict

#Finaliza reporte de frecuencias grupales

def reporte_comp_diagnostico(request):
    conexiones = User.objects.all()

    context = {
        'conexiones': conexiones,
    }

    return render(request, 'reporte_comp_diagnostico.html', context)

def reporte_est_superficie(request):
    conexiones = User.objects.all()

    context = {
        'conexiones': conexiones,
    }

    return render(request, 'reporte_est_superficie.html', context)

def reporte_clas_severidad(request):
    conexiones = User.objects.all()

    context = {
        'conexiones': conexiones,
    }

    return render(request, 'reporte_clas_severidad.html', context)

def reporte_clas_pacientes(request):
    conexiones = User.objects.all()

    context = {
        'conexiones': conexiones,
    }

    return render(request, 'reporte_clas_pacientes.html', context)

def reporte_nec_trat_svariable(request):
    conexiones = User.objects.all()

    context = {
        'conexiones': conexiones,
    }

    return render(request, 'reporte_nec_trat_var.html', context)


def reporte_pac_atendidos(request):
    conexiones = User.objects.all()

    context = {
        'conexiones': conexiones,
    }

    return render(request, 'reporte_pac_atendidos.html', context)

def reporte_frecuencias(request):
    conexiones = User.objects.all()

    context = {
        'conexiones': conexiones,
    }

    return render(request, 'reporte_frecuencias.html', context)

def reporte_prevalencias(request):
    conexiones = User.objects.all()

    context = {
        'conexiones': conexiones,
    }

    return render(request, 'reporte_prevalencias.html', context)

def reporte_nec_tratamiento(request):
    conexiones = User.objects.all()

    context = {
        'conexiones': conexiones,
    }

    return render(request, 'reporte_nec_tratamiento.html', context)

def reporte_severidad(request):
    conexiones = User.objects.all()

    context = {
        'conexiones': conexiones,
    }

    return render(request, 'reporte_severidad.html', context)
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
            "allowHTML":"true"
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
            "name":"Parámetro",
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