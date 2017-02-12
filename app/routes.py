from flask import Flask, render_template, jsonify
from bills import *

app = Flask(__name__)      

@app.route('/')
def home():
  return render_template('home.html')

@app.route('/api/get_recent')
def get_recent_api():
  return get_all_recent_bills()

@app.route('/signup')
def signup():
	return render_template('layout.html')

if __name__ == '__main__':
  app.run(debug=True)