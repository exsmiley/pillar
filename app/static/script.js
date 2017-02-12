
var apiURL = 'http://localhost:5000/api/get_recent';

$(document).ready(function(){
var categories=["  Agriculture and Food",
"Animals",
"Armed Forces and National Security",
"Arts, Culture, Religion",
"Civil Rights and Liberties, Minority Issues",
"Commerce",
"Congress",
"Crime and Law Enforcement",
"Economics and Public Finance",
"Education",
"Emergency Management",
"Energy",
"Environmental Protection",
"Families",
"Finance and Financial Sector",
"Foreign Trade and International Finance",
"Government Operations and Politics",
"Health",
"Housing and Community Development",
"Immigration",
"International Affairs",
"Labor and Employment",
"Law",
"Native Americans",
"Public Lands and Natural Resources",
"Science, Technology, Communications",
"Social Sciences and History",
"Social Welfare",
"Sports and Recreation",
"Taxation",
"Transportation and Public Works",
"Water Resources Development",
]


$.each(categories,function(index,value){
    var checkbox="<input type='checkbox' class='x' value="+value+" name="+value+" style='padding-left: 10px; padding-right: 10px;'><label for="+value+">"+value+"</label> <br>"
    $(".checkBoxContainer").append($(checkbox));
})


$(function() {
    $('button').click(function() {
        var user = $('#txtUsername').val();
        var pass = $('#txtPassword').val();
        var confirmPass = $('#txtconfirmPassword').val();
        var state = $('#txtState').val();
/*        $.ajax({
            url: '/signUp',
            data: $('form').serialize(),
            type: 'POST',
            success: function(response) {
                console.log(response);
            },
            error: function(error) {
                console.log(error);
            }
        });*/

        var dataList = document.getElementById('state');
        var input = document.getElementById('ajax');

        $.ajax({
            url: '{{ url_for("autocomplete") }}'
            }).done(function (data) {
                $('#autocomplete').autocomplete({
                    source: data.json_list,
                    minLength: 2
                });
            });
        });
    });
});