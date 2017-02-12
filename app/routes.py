from flask import Flask, render_template, request, jsonify, make_response, session, redirect, url_for
import hashlib
import os
import json
from bills import *
from dbagent import *

app = Flask(__name__) # Pillar12!

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
        return redirect('/dashboard')
    return render_template('home.html')

@app.route('/signup')
def signup_render():
    if 'username' in session:
        return redirect('/dashboard')
    return render_template('signup.html')

@app.route('/logout')
def logout():
    del session['username']
    return redirect('/')

# sign up/login
@app.route('/api/signup', methods=['POST'])
def signup():
    name, email, phone, zipcode, pwd = request.json['name'], request.json['email'], request.json['phone'], request.json['zipcode'], request.json['password']
    new_acc = add_new_user(email, pwd, phone, zipcode, name)
    if new_acc:
        session['username'] = email
        add_topics_for_user(email, request.json['topics'])
        try:
            text_sign_up(email) # fail if invalid phone number
        except:
            pass
        return redirect('/')
    else:
        return redirect('/signup')


@app.route('/api/login', methods=['POST'])
def login():
    email, pwd = request.json['email'], request.json['password']
    new_acc = validate_user(email, pwd)
    if new_acc:
        session['username'] = email

        return redirect('/dashboard')
    else:
        return redirect('/')

@app.route('/dashboard', methods=['POST', 'GET'])
def dashboard():
    if not 'username' in session:
        return redirect('/')
    return render_template('dashboard.html')

@app.route('/act', methods=['POST', 'GET'])
def act():
    if not 'username' in session:
        return redirect('/')
    return render_template('act.html')

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
    email = session['username']
    get_topics_for_user(email)

@app.route('/api/update_topics', methods=['POST'])
def update_topics():
    email, topics = session['username'], request.form['topics']
    add_topics_for_user(email, topics)

@app.route('/api/get_recent')
def get_recent_api():
    return get_all_recent_bills()

@app.route('/api/get_me_recent')
def get_recent_me():
    email = session['username']
    com = json.loads(get_recent_bills_by_committee())
    topics = set(json.loads(get_topics_for_user(email)))
    relevant = []
    for c, v in com.iteritems():
        if c in topics:
            relevant.append(v)

    return jsonify({"recent": relevant})

@app.route('/api/get_me_reps')
def get_reps_me():
    email = session['username']
    zipcode = user_zipcode(email)
    return jsonify({"reps": get_my_reps(zipcode)})

@app.route('/api/test', methods=['POST'])
def tester():
    return jsonify(request.json)

@app.route('/viz')
def viz():
    return render_template('viz2.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
