from flask import Flask

task = Flask(__name__)

@task.route('/')
def homepage():
	return "Flask is up"