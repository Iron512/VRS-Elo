import requests
import os
import json

access_token = str(os.environ.get('ACCESS_TOKEN'))

r = requests.get('https://vrselo.herokuapp.com/rawdata/', params="code=22e5293f4cca593ddc7bcc180cc938bf")
print(r.text)