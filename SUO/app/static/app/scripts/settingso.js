$(document).ready(function () {
    $.ajax({
        url: "settingsotable",
        method: 'GET',
        data: {
            click: true
        },
        success: function (response) {
            for (i = 0; i < response.window.length; i++) {
                $('table').prepend('<tr><td class="table1">Окно: ' + response.window[i] + '</td></tr>');
            }
        }
    });
});