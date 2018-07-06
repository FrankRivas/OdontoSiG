var datos1 = [];
var datos2 = [];
var datos3 = [];
var datos4 = [];
var ward = 0;
var higher = 0;

for(var i1 = 0; i1 < cpod.length; i1++) {
    if(cpod[i1].estado != "Total") {
        datos1.push({
            name: cpod[i1].estado,
            y: cpod[i1].cantidad
        });
    }
}

for(var i2 = 0; i2 < ceod.length; i2++) {
    if(ceod[i2].estado != "Total") {
        datos2.push({
            name: ceod[i2].estado,
            y: ceod[i2].cantidad
        });
    }
}

for(var i3 = 0; i3 < cpom.length; i3++) {
    if(cpom[i3].estado != "Total") {
        datos3.push({
            name: cpom[i3].estado,
            y: cpom[i3].cantidad
        });
    }
}

for(var i4 = 0; i4 < cpos.length; i4++) {
    if(cpos[i4].estado != "Total") {
        datos4.push({
            name: cpos[i4].estado,
            y: cpos[i4].cantidad
        });
    }
}

var temporal = [datos1, datos2, datos3, datos4];
for(var j = 0; j < 4; j++) {
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
            sourceWidth: 750,
            filename: "Informe_Frencuencias",
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
                center: [ 170, 140 ],
                type: "pie",
                name: "Parametro",
                data: datos1
            },
            {
                center: [ 520, 140],
                type: "pie",
                name: "Parametro",
                data: datos2
            },
            {
                center: [ 170, 400 ],
                type: "pie",
                name: "Parametro",
                data: datos3
            },
            {
                center: [ 520, 400 ],
                type: "pie",
                name: "Parametro",
                data: datos4
            }
        ]
}, function(chart) {
    var newX = chart.plotWidth / 2 + chart.plotLeft;
    var newY = chart.plotHeight / 2 + chart.plotTop;
    chart.renderer.image(logo, 120, 25, 130, 130).add();
    chart.renderer.text("UNIVERSIDAD DE EL SALVADOR", 280, 60).css({
        fontSize: "18px"
    }).add();
    chart.renderer.text('FACULTAD DE ODONTOLOGÍA', 280, 90).css({
        fontSize: "18px"
    }).add();
    chart.renderer.text('SCSAB-FOUES', 280, 120).css({
        fontSize: "18px"
    }).add();
    chart.renderer.text("CPOD", 190, 340).add();
    chart.renderer.text("ceod", 530, 340).add();
    chart.renderer.text("CPOM",190, 590).add();
    chart.renderer.text("CPOS",520, 590).add();
    chart.setTitle({text:"<div class='col s12'>" +
        "<div class='offset-s4'><p class='center-align'>INFORME DE FRECUENCIAS GRUPALES</p></div></div>"});
    if(flag == true) {
        chart.setSubtitle({text: "<div class='col s12'>" +
            "<div class='row'><p class='center-align'>Datos desde:" + desde + " hasta: " + hasta + "</p><br></div>" +
            "<div class='row'><p class='center-align'>Según criterio "+ $("#criterio option[value='" + parametros.criterio + "']").text() + "</p></div>" +
            "</div>"});
    } else {
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

