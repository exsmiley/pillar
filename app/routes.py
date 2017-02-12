from flask import Flask, render_template, request, jsonify, make_response
from bills import *
from dbagent import *

app = Flask(__name__, static_url_path='/static')      

@app.route('/')
def home():
    username = request.cookies.get('username')
    if username:
        return redirect("/main", code=302)
    return render_template('home.html')

@app.route('/signup')
def signup_render():
    return render_template('signup.html')


# sign up/login
@app.route('/api/signup', methods=['POST'])
def signup():
    name, pwd, phone = request.form['name'], request.form['pwd'], request.form['phone']
    new_acc = add_new_user(email, pwd, phone)
    if new_acc:
        return redirect("/main", code=302)
    else:
        return render_template('home.html')

@app.route('/api/login', methods=['POST'])
def login():
    name, pwd = request.form['name'], request.form['pwd']
    new_acc = validate_user(email, pwd, phone)
    if new_acc:
        return redirect("/main", code=302)
    else:
        return render_template('home.html')


# other API functions
@app.route('/api/update_topics', methods=['POST'])
def update_topics():
    name, topics = request.form['name'], request.form['topics']
    add_topics_for_user(email, topics)

@app.route('/api/get_recent')
def get_recent_api():
    return get_all_recent_bills()
  

if __name__ == '__main__':
    app.run(debug=True)