from flask import Flask, render_template, request, jsonify
from bills import *

app = Flask(__name__)      

@app.route('/')
def home():
    return render_template('home.html')

# sign up/login
@app.route('/api/signup', methods=['POST'])
def signup():
    # if not request.data:
    #     abort(400)

    print "Dudeeee", request.form['name'], request.form['pwd']
    return render_template('layout.html')

@app.route('/api/get_recent')
def get_recent_api():
    return get_all_recent_bills()

@app.route('/signup')
def signup_render():
	return render_template('signup.html')
  

if __name__ == '__main__':
    app.run(debug=True)