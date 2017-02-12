from flask import Flask, render_template, request, jsonify, make_response, session, redirect, url_for
import hashlib
from bills import *
from dbagent import *

app = Flask(__name__)

# set the secret key.  keep this really secret:
app.secret_key = hashlib.sha256("I'm a cool bruh").hexdigest()

@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r

@app.route('/')
def home():
    if 'username' in session:
        return render_template("dashboard.html")
    return render_template('home.html')

@app.route('/signup')
def signup_render():
    return render_template('signup.html')

@app.route('/logout')
def logout():
    del session['username']
    return redirect('/')


# sign up/login
@app.route('/api/signup', methods=['POST'])
def signup():
    name, pwd, phone, zipcode = request.json['email'], request.json['email'], request.json['phone'], request.json['zipcode']
    new_acc = add_new_user(email, pwd, phone, zipcode)
    if new_acc:
        session['username'] = request.form['name']
        return jsonify({"route": "/"})
    else:
        return jsonify({"route": "/signup"})

@app.route('/api/login', methods=['POST'])
def login():
    email, pwd = request.json['email'], request.json['password']
    new_acc = validate_user(email, pwd)
    if new_acc:
        session['username'] = request.json['email']

        return jsonify({"route": "/dashboard"})
        # return redirect("/dashboard", code=302)
    else:
        return jsonify({"route": "/"})
        # return render_template('home.html')

@app.route('/dashboard', methods=['POST', 'GET'])
def dashboard():
    #name, pwd, phone = request.form['name'], request.form['pwd'], request.form['phone']
    #new_acc = add_new_user(email, pwd, phone)
    #if new_acc:
    #    return redirect("/main", code=302)
    #else:
    return render_template('dashboard.html')

@app.route('/legislation', methods=['POST', 'GET'])
def legislation():
    #name, pwd, phone = request.form['name'], request.form['pwd'], request.form['phone']
    #new_acc = add_new_user(email, pwd, phone)
    #if new_acc:
    #    return redirect("/main", code=302)
    #else:
    return render_template('legislation.html')

# other API functions
@app.route('/api/get_topics')
def get_topics():
    email, topics = session['username'], request.form['topics']
    add_topics_for_user(email, topics)

@app.route('/api/update_topics', methods=['POST'])
def update_topics():
    email, topics = session['username'], request.form['topics']
    add_topics_for_user(email, topics)

@app.route('/api/get_recent')
def get_recent_api():
    return get_all_recent_bills()

@app.route('/api/test', methods=['POST'])
def tester():
    print request.json
    return jsonify(request.json)
  

if __name__ == '__main__':
    app.run(debug=True)