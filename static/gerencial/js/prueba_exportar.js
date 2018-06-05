

function crear() {
    $.ajax({
        url: 'ajax/prueba_creacion',
        dataType: 'json',
        success: function(data) {
            console.log(data);
            Highcharts.chart("container", data);
        },
        error: function(data) {
            console.log("data");
        }
    });
}