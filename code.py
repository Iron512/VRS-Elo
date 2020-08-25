import json
import sys

def load_raw(): 
    with open("data.json") as fi:
        raw_data = json.load(fi)
    
    return raw_data

def store_raw(data):
    with open('data.json', 'w') as fo:
        json.dump(data, fo)