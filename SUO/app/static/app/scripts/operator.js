$('#Next').click(function () {
    $.ajax({
        url: "nextbutton",
        method: 'GET', // or another (GET), whatever you need
        data: {
            click: true
        },
        success: function (response) {
            $('#ta').text(response.ticket);
            // success callback
            // you can process data returned by function from views.py
        }
    });
});