

function crear() {
    $.ajax({
        url: 'ajax/prueba_creacion',
        dataType: 'json',
        success: function(data) {
            var fn = Function(data.render.dataLabelFunction);
            data.chart.plotOptions.pie.dataLabels = {"formatter": fn};
            Highcharts.chart("container", data.chart, function (chart) {
                chart.renderer.image(data.render.image, 30, 25, 130, 130).add();
                chart.renderer.text("UNIVERSIDAD DE EL SALVADOR", 200, 60).css({
                    fontSize: "18px"
                })
                .add();
                chart.renderer.text('FACULTAD DE ODONTOLOGÍA', 200, 90).css({
                    fontSize: "18px"
                })
                .add();
                chart.renderer.text('SCSAB-FOUES', 200, 120).css({
                    fontSize: "18px"
                })
                .add();
                chart.setTitle({text:"<div class='col s12'>" +
                                            "<div class='offset-s4'><p class='center-align'>" + data.render.titulo + "</p></div>" +
                                    "</div>"});
                chart.setSubtitle({text:"<div class='col s12'>" +
                    "<div class='offset-s3'><p class='center-align'>" + data.render.periodo + "</p></div>" +
                "</div>"});
            });
        },
        error: function(data) {
            console.log("data");
        }
    });
}