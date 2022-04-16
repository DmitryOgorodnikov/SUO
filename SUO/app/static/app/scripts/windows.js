$('#id_id_window').mouseenter(function () {
    $.ajax({
        url: "windowbutton",
        method: 'GET', // or another (GET), whatever you need
        data: {
            click: true
        },
        success: function (response) {
            $('#id_id_window option').remove();
            for (var i = 0; i < response.windows_l.length; i++) {
                $('#id_id_window').prepend('<option value="'+ (i+1) +'">' + response.windows_l[i] + '</option>');
            }
            // success callback
            // you can process data returned by function from views.py
        }
    });
});

$(function () {
    $.ajax({
        url: "windowbutton",
        method: 'GET', // or another (GET), whatever you need
        data: {
            click: true
        },
        success: function (response) {
            localStorage.clear();
            $('#id_id_window option').remove();
            for (var i = 0; i < response.windows_l.length; i++) {
                $('#id_id_window').prepend('<option value="' + (i + 1) + '">' + response.windows_l[i] + '</option>');
            }
            // success callback
            // you can process data returned by function from views.py
        }
    });
});