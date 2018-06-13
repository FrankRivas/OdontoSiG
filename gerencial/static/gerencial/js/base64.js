function to_data_url(src, callback) {
    var xhttp = new XMLHttpRequest();
    xhttp.onload = function() {
        var fileReader = new FileReader();
        fileReader.onloadend = function() {
            callback(fileReader.result);
            }
            fileReader.readAsDataURL(xhttp.response);
        };

    xhttp.responseType = 'blob';
    xhttp.open('GET', src, true);
    xhttp.send();
}
