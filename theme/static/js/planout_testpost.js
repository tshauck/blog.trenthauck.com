jQuery(document).ready(function($) {

    var clientId = localStorage.getItem('clientId');

    if (clientId == null) {
        clientId = '' + Math.floor((Math.random() * 100000) + 1);
        localStorage.setItem('clientId', clientId);
        ga('set', 'dimension3', clientId);
    }

    var api = "http://162.243.42.182:8999/testpost/".concat(clientId);
    console.log(api);

    $.ajax({
            url : api,
            type: 'GET',
            dataType: 'jsonp',
            jsonpCallback: "localcallback",
            success: function (data) {
                var data = $.parseJSON(data);

                $("#twitter").html(data["action_text"]);

            }
    })

});
