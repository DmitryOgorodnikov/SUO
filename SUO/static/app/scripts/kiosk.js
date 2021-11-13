$('#buttonSend').click(function () {
    $.ajax({
        url: "{% url 'kbutton' %}",
        method: 'POST', // or another (GET), whatever you need
        data: {
            click: true
        },
        success: function (data) {
            // success callback
            // you can process data returned by function from views.py
        }
    });
});