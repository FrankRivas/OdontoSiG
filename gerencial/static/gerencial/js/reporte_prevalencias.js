var datos1 = [];
var datos2 = [];
var datos3 = [];
var datos4 = [];
var datos5 = [];
var higher = 0;
var ward = 0;

for(var i1 = 0; i1 < cposd.length; i1++) {
    datos1.push({
        name: cposd[i1].estado,
        y: cposd[i1].cantidad
    });
}

for(var i2 = 0; i2 < cpose.length; i2++) {
    datos2.push({
        name: cpose[i2].estado,
        y: cpose[i2].cantidad
    });
}

for(var i3 = 0; i3 < cpod.length; i3++) {
    datos3.push({
        name: cpod[i3].estado,
        y: cpod[i3].cantidad
    });
}

for(var i4 = 0; i4 < ceod.length; i4++) {
    datos4.push({
        name: ceod[i4].estado,
        y: ceod[i4].cantidad
    });
}

for(var i5 = 0; i5 < cpom.length; i5++) {
    datos5.push({
        name: cpom[i5].estado,
        y: cpom[i5].cantidad
    });
}

var temporal = [datos1, datos2, datos3, datos4, datos5];
for(var j = 0; j < 5; j++) {
    if(temporal[j].length > ward) {
        ward = temporal[j].length
        higher = j;
    }
}

Highcharts.setOptions({
    lang: {
        downloadPNG: "Descargar en formato PNG",
        downloadPDF: "Descargar en formato PDF",
        downloadJPEG: "Descargar en formato JPEG"
    }
});
Highcharts.chart("container", {
        chart: {
            //Tipo de gráfico y espacio de header
            type:"pie",
            spacingTop: 200
        },
        //Mantiene el formato de html en la exportación
        exporting:{
            enabled:true,
            allowHTML:true,
            filename: "Informe_Prevelencias",
            buttons: {
                contextButton: {
                    menuItems: [ "downloadPNG", "downloadPDF", "downloadJPEG"]
                }
            }
        },
        tooltip: {
            shared: true
        },
        plotOptions:{
            //Tamaño del diámetro del gráfico
            pie: {
                size:100
            },
            //Opciones de labels en el gráfico
            series: {
                dataLabels:{
                    align:"left",
                    enabled:true,
                    formatter: function() {
                        return this.point.name+':'+this.percentage.toFixed(1)+'%';
                    }
                }
            }
        },
        legend:{
            enabled:true,
            align:"center"
        },
        //Información en base a la que se construye el gráfico
        series: [
            {
                center: [ 150, 140 ],
                type: "pie",
                name: "Parametro",
                data: datos1
            },
            {
                center: [ 400, 140],
                type: "pie",
                name: "Parametro",
                data: datos2
            },
            {
                center: [ 150, 350 ],
                type: "pie",
                name: "Parametro",
                data: datos3
            },
            {
                center: [ 400, 350 ],
                type: "pie",
                name: "Parametro",
                data: datos4
            },
            {
                center: [ 150, 510 ],
                type: "pie",
                name: "Parametro",
                data: datos5
            }
        ]
}, function(chart) {
    chart.renderer.image(logo, 30, 25, 130, 130).add();
    chart.renderer.text("UNIVERSIDAD DE EL SALVADOR", 200, 60).css({
        fontSize: "18px"
    }).add();
    chart.renderer.text('FACULTAD DE ODONTOLOGÍA', 200, 90).css({
        fontSize: "18px"
    }).add();
    chart.renderer.text('SCSAB-FOUES', 200, 120).css({
        fontSize: "18px"
    }).add();
    chart.renderer.text("CPOS + CPOD", 130, 320).add();
    chart.renderer.text("CPOS + ceod", 390, 320).add();
    chart.renderer.text("CPOD",150, 530).add();
    chart.renderer.text("ceod",400, 530).add();
    chart.renderer.text("CPOM",150, 710).add();
    chart.setTitle({text:"<div class='col s12'>" +
        "<div class='offset-s4'><p class='center-align'>INFORME DE PREVALENCIA</p></div></div>"});
    if(flag == true) {
        var fi = new Date(parametros.fecha_desde);
        var fh = new Date(parametros.fecha_hasta);
        fi = new Intl.DateTimeFormat("en-GB").format(fi);
        fh = new Intl.DateTimeFormat("en-GB").format(fh);
        chart.setSubtitle({text: "<div class='col s12'>" +
            "<div class='row'><p class='center-align'>Datos desde:" + fi + " hasta: " + fh + "</p><br></div>" +
            "<div class='row'><p class='center-align'>Según criterios: "+ $("#criterio option[value='" + parametros.criterio + "']").text() + "</p></div>" +
            "</div>"});
    }else {
        chart.setSubtitle({text:"<div class='col s12'>" +
        "<div class='offset-s3'><p class='center-align'>Datos de muestra</p></div></div>"});
    }
    chart.series[higher].update({ showInLegend: true, shared: true });
    $(chart.series[higher].data).each(function(i, e) {
            e.legendItem.on('click', function(event) {
                var legendItem=e.name;

                $(chart.series).each(function(j,f){
                       $(this.data).each(function(k,z){
                           if(z.name==legendItem)
                           {
                               if(z.visible)
                               {
                                   z.setVisible(false);
                               }
                               else
                               {
                                   z.setVisible(true);
                               }
                           }
                       });
                });

            });
        });
});



