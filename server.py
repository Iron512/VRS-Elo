from flask import Flask, request, session, redirect, url_for, render_template
from code import *

import os
import json

task = Flask(__name__)
access_token = str(os.environ.get('ACCESS_TOKEN'))
visualization_token = str(os.environ.get('VISUALIZATION_TOKEN'))
session_secret_key = str(os.environ.get('SESSION_SECRET_KEY'))
task.secret_key = session_secret_key

data = {}

@task.route('/')
def index(data=data):
    if data == {}:
        #loads data from the standard defined json file
        data = load_raw()

    return render_template("index.html", visualization_token=visualization_token)

@task.route('/update/', methods=['GET'])
def update(data=data):
    if data == {}:
        data = load_raw()
    
    #k factor and evaluation matrix is loaded
    kfactor = data["k-factor"]
    keval = data["evaluation"]

    if request.args.get('code') == None:
        return "<h2>This area is forbidden without a code</h2>"

    code = request.args.get('code')
    if code != access_token:
        return "<h2>The code "+code+" is not correct<h2>"

    #code is correct, we can perform the operation

    match = {
      "law": [
        "Ivan",
        "Paco"
      ],
      "out": [
        "Gianler",
        "Morens"
      ],
      "ren": [
        "Gian"
      ],
      "win": "law",
      "alive": [
        "Ivan",
        "Morens"
      ]
    }

    data = update_ratings(data, keval, kfactor, match)
    store_raw(data)

    return redirect(url_for('index'))

@task.route('/rawdata/', methods=['GET'])
def get_rawdata(data=data):
    if data == {}:
        data = load_raw()

    if request.args.get('code') == None:
        return "<h2>This area is forbidden without a code</h2>"

    code = request.args.get('code')
    if code != visualization_token:
        return "<h2>The code "+code+" is not correct<h2>"

    return json.dumps(data)

