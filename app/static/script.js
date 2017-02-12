
Vue.use(VueRouter);

var router = new VueRouter() ;
var apiURL = 'http://localhost:5000/api/get_recent';

var loginapp = new Vue ({
    el: '#loginapp',
    data: {
        email: "",
        password: ""
    },
    methods: {
        onSubmit: function(e) {
            this.$http.post('/api/login', JSON.stringify({"email": this.email, "password": this.password})).then(function(post){
                console.log(post['body']['route'])
                var r = post['body']['route']
                router.go(r)
                /// Something like.... router.redirect('/')
            });
        }
    },
    delimiters: ['{/', '/}']
})

var signupapp = new Vue ({
    el: '#signupapp',
    data: {
        name: "",
        email: "",
        phone: "",
        zip: "",
        password: ""
    },
    methods: {
        registerUser: function(e) {
            this.$http.post('/api/signup', JSON.stringify({
                "name": this.name,
                "email": this.email,
                "phone": this.phone,
                "zipcode": this.zipcode,
                "password": this.password})).then(function(post){
                
                /// Something like.... router.redirect('/')
            });
        }
    }

})

var app4 = new Vue({
  el: '#app-4',
  data: {
    bills: [
      { text: 'i am a bill' },
      { text: 'i am a bill too' },
      { text: 'oops wrong place i am a bob' }
    ]
  },
  delimiters: ['{/', '/}']
})

$(document).ready(function(){
    var categories = ['Ways and Means', 'Oversight and Government Reform', 'Natural Resources', 'Energy and Natural Resources', 'Indian Affairs', 'Small Business and Entrepreneurship', 'Transportation and Infrastructure', 'Administration', 'Judiciary', 'Homeland Security and Governmental Affairs', 'Energy and Commerce', 'Health, Education, Labor, and Pensions', 'Banking, Housing, and Urban Affairs', "Veterans' Affairs", 'Commerce, Science, and Transportation', 'Education and the Workforce', 'Armed Services', 'Agriculture', 'Foreign Relations', 'Finance']
    $.each(categories,function(index,value){
        var checkbox="<input type='checkbox' class='x' value="+value+" name="+value+" style='padding-left: 10px; padding-right: 10px;'><label for="+value+">"+value+"</label> <br>"
        $(".checkBoxContainer").append($(checkbox));
    })
}

/*
$(function() {
    $('button').click(function() {
        var user = $('#txtUsername').val();
        var pass = $('#txtPassword').val();
        var confirmPass = $('#txtconfirmPassword').val();
        var state = $('#txtState').val();
        $.ajax({
            url: '/signUp',
            data: $('form').serialize(),
            type: 'POST',
            success: function(response) {
                console.log(response);
            },
            error: function(error) {
                console.log(error);
            }
        });

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
});*/