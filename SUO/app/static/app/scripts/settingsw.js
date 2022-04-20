$(document).ready(function () {
    $.ajax({
        url: "settingswtable",
        method: 'GET',
        data: {
            click: true
        },
        success: function (response) {
            for (i = response.window.length-1; i >= 0; i--) {
                $('table').prepend('<tr><td class="table1">Окно: ' + response.window[i] + '</td></tr>');
            }
        }
    });
});