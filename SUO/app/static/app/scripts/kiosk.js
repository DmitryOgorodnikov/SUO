$('#buttonSend').click(function () {
    $.ajax({
        url: "kbutton",
        method: 'POST', // or another (GET), whatever you need
        data: {
            name: 'S',
            click: true
        },
        success: function (data) {
            // success callback
            // you can process data returned by function from views.py
        }
    });
});

$('#buttonReceive').click(function () {
    $.ajax({
        url: "kbutton",
        method: 'POST', // or another (GET), whatever you need
        data: {
            name: 'R',
            click: true
        },
        success: function (data) {
            // success callback
            // you can process data returned by function from views.py
        }
    });
});