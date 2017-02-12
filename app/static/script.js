var apiURL = 'http://localhost:5000/api/get_recent';


$(function() {
    $('button').click(function() {
        var user = $('#txtUsername').val();
        var pass = $('#txtPassword').val();
        $.ajax({
            url: '/home',
            data: $('form').serialize(),
            type: 'POST',
            success: function(response) {
                console.log(response);
            },
            error: function(error) {
                console.log(error);
            }
        });
    });
    $('#signup').click(function() {
        window.location = "www.example.com/index.php?id=" + this.id;
    })
});