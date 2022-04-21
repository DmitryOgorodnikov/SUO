$(document).ready(function () {
    $.ajax({
        url: "settingstable",
        method: 'GET',
        data: {
            click: true
        },
        success: function (response) {
            for (i = 0; i < response.user.length; i++) {
                $('table').prepend('<tr><td class="table1">Логин: ' + response.user[i][1] + '</td>' + '<td class="table2">ФИО: ' + response.user[i][2] +
                    '</td><td class="table3"></td> <td class="table4"> <input type="button" class="btn btn-default btn-index" name= "' +
                    response.user[i][0] + '" value="Настроить" id="Edit"> </td> <td class="table4"> <input type="button" class="btn btn-default btn-index" name= "' +
                    response.user[i][0] + '" value="Удалить" id="Del"></td> </tr>');
            }
        }
    });
});

$('table').on('click', '#Del', function () {
    $.ajax({
        url: "delbutton",
        method: 'GET',
        data: {
            idbutton: this.name,
            click: true
        },
        success: function (response) {
            location.reload();
        }
    });
});

$('table').on('click', '#Edit', function () {
    $.ajax({
        url: "edituser",
        method: 'GET',
        data: {
            idbutton: this.name,
            click: true
        },
        success: function (response) {
            window.location.href = "../editer"
        }
    });
});