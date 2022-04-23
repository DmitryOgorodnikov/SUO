$(document).ready(function () {
    $.ajax({
        url: "kioskbtn",
        method: 'GET',
        data: {
            click: true
        },
        success: function (response) {
            arr = response.serviceslist;
            arr.reverse();
            arr.forEach(function (item, i, arr) {
                if (item['status'] != true)
                    delete arr[i]
                else
                    $('.kiosk-div').prepend('<div class="kiosk-div-button settings-btn" id="buttonticket" name="' + item['rusname'] +'"><p>' + item['rusname'] +'</p></div>');
            });
        }
    });
});

$('.kiosk-div').on('click', '#buttonticket', function () {
    $.ajax({
        url: "kbutton",
        method: 'POST',
        data: {
            name: $(this).attr("name"),
            click: true
        },
        success: function (data) {

        }
    });
});