from flask import Flask, request, session, redirect, url_for
from code import *

import os

task = Flask(__name__)
access_token = str(os.environ.get('ACCESS_TOKEN'))
session_secret_key = str(os.environ.get('SESSION_SECRET_KEY'))
task.secret_key = session_secret_key

data = {}

@task.route('/')
def homepage(data=data):
    if data == {}:
        data = load_raw()

    return str(data["first"])

@task.route('/set/', methods=['GET'])
def set(data=data):
    if request.args.get('code') == None:
        return "<h2>This area is forbidden without a code</h2>"

    code = request.args.get('code')
    if code != access_token:
        return "<h2>The code "+code+" is not correct<h2>"

    #code is correct, we can perform the operation
    if request.args.get('value') != None:
        value = request.args.get('value')
        data["first"] = int(value)

        store_raw(data)


    return redirect(url_for('homepage'))

@task.route('/rawdata/', methods=['GET'])
def get_rawdata(data=data):
    if request.args.get('code') == None:
        return "<h2>This area is forbidden without a code</h2>"

    code = request.args.get('code')
    if code != access_token:
        return "<h2>The code "+code+" is not correct<h2>"

    return str(data)