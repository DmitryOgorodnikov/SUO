$('#Next').click(function () {
    $.ajax({
        url: "nextbutton",
        method: 'POST',
        data: {
            click: true
        },
        success: function (response) {
            var text = response.ticket;
            $('#ta').text(text);
        }
    });
});