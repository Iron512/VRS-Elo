from flask import Flask, request, session, redirect, url_for, render_template, jsonify
from code import *

import os
import json

task = Flask(__name__)
access_token = str(os.environ.get('ACCESS_TOKEN'))
visualization_token = str(os.environ.get('VISUALIZATION_TOKEN'))

data = {}

@task.route('/')
def index(data=data):
    if data == {}:
        #loads data from the standard defined json file
        data = load_raw()

    return render_template("index.html", visualization_token=visualization_token)

@task.route('/update/', methods=['POST'])
def update(data=data):
    if data == {}:
        data = load_raw()
    
    #k factor and evaluation matrix is loaded
    kfactor = data["k-factor"]
    keval = data["evaluation"]

    if request.get_json()['code'] == None:
        return "<h2>This area is forbidden without a code</h2>"

    code = request.get_json()['code']
    if code != access_token:
        return "<h2>The code "+code+" is not correct<h2>"

    #code is correct, we can perform the operation

    match = request.get_json()['match']

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

