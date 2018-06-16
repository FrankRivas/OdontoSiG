
var datos = [];

for(var i = 0; i < severidad.length; i++) {
    datos.push({
        name: severidad[i].severidad,
        y: severidad[i].afectados
    });
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
            filename: "Informe_Severidad_Caries",
            buttons: {
                contextButton: {
                    menuItems: [ "downloadPNG", "downloadPDF", "downloadJPEG"]
                }
            }
        },
        plotOptions:{
            //Tamaño del diámetro del gráfico
            pie: {
                size:250
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
        series: [{
            showInLegend:true,
            name: "Parámetro de dato",
            data:datos
        }]
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
    chart.setTitle({text:"<div class='col s12'>" +
        "<div class='offset-s4'><p class='center-align'>INFORME DE SEVERIDAD DE CARIES</p></div></div>"});
    if(flag == true) {
        var fi = new Date(parametros.fecha_desde);
        var fh = new Date(parametros.fecha_hasta);
        fi = new Intl.DateTimeFormat("en-GB").format(fi);
        fh = new Intl.DateTimeFormat("en-GB").format(fh);
        chart.setSubtitle({text: "<div class='col s12'>" +
            "<div class='row'><p class='center-align'>Datos desde:" + fi + " hasta: " + fh + "</p><br></div>" +
            "<div class='row'>" +
            "<p class='center-align'>Según sexo: "+ $("#sexo option[value='" + parametros.sexo + "']").text() +
            ",residencia: "+ $("#residencia option[value='" + parametros.residencia + "']").text() +
            ", grupo etario:  "+ $("#etario option[value='" + parametros.etario + "']").text() +
            "</p></div>" +
            "</div>"});
    } else {
        chart.setSubtitle({text:"<div class='col s12'>" +
        "<div class='offset-s3'><p class='center-align'>Datos de muestra</p></div></div>"});
    }
});
