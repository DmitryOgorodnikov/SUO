$(document).ready(function () {
    $.ajax({
        url: "settingstable",
        method: 'GET',
        data: {
            click: true
        },
        success: function (response) {
            for (i = 0; i < response.user.length; i++) {
                $('table').prepend('<tr><td class="table1">Логин: ' + response.user[i][1] + '</td>' + '<td class="table2">ФИО: ' + response.user[i][2] + '</td><td class="table3"></td> <td class="table4"></td> <td class="table4"></td> </tr>')
            }
        }
    });
});