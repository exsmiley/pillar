
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
        zipcode: "",
        password: "",
        url: '/signup',
        categories : ['Ways and Means', 'Oversight and Government Reform', 'Natural Resources', 'Energy and Natural Resources', 'Indian Affairs', 'Small Business and Entrepreneurship', 'Transportation and Infrastructure', 'Administration', 'Judiciary', 'Homeland Security and Governmental Affairs', 'Energy and Commerce', 'Health, Education, Labor, and Pensions', 'Banking, Housing, and Urban Affairs', "Veterans' Affairs", 'Commerce, Science, and Transportation', 'Education and the Workforce', 'Armed Services', 'Agriculture', 'Foreign Relations', 'Finance'],
        selected : []
    },
    methods: {
        registerUser: function(e) {
            this.$http.post('/api/signup', JSON.stringify({
                "name": this.name,
                "email": this.email,
                "phone": this.phone,
                "zipcode": this.zipcode,
                "topics": this.selected,
                "password": this.password,})).then(function(post){
                this.url = '/'
                console.log(this.url)
                router.go(this.url)
                /// Something like.... router.redirect('/')
            }).catch(function() {
                    alert("AHHHH")
                });
        },
        toggle: function(category) {
            var i = this.selected.indexOf(category)
            if( i >= 0) {
                this.selected.splice(i, 1);
            }
            else {
                this.selected.push(category)
            }
        }
    },
    delimiters: ['{/', '/}']
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

var upcoming = new Vue({
  el: '#upcoming',
  data: {
    bills: []
  },
  methods: {
    loadBills: function() {
        this.$http.get('/api/get_me_recent').then(function(res) {
            this.bills = res['body']['recent']
        });
    }
  },
  delimiters: ['{/', '/}']
})

upcoming.loadBills();

