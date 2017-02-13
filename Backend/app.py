from flask import Flask
from flask_pymongo import PyMongo
import config

import json

app = Flask(__name__)

app.config['MONGO_DBNAME'] = config.mongouser
app.config['MONGO_URI'] = config.mongouri

mongo = PyMongo(app)


@app.route('/')

def load_json_multiple(segments):
    chunk = ""

    for segment in segments:
        chunk += segment
        try:
            yield json.loads(chunk)
            chunk = ""
        except ValueError:
            pass

path = "C:\\Users\\Omppu\\PycharmProjects\\Game_Analytic_Software_for_Serious_Games\\Backend\\JSONs\\logs.json"

def change_keys(obj, convert):

    if isinstance(obj, (str, int, float)):
        return obj
    if isinstance(obj, dict):
        new = obj.__class__()
        for k, v in obj.items():
            new[convert(k)] = change_keys(v, convert)
    elif isinstance(obj, (list, set, tuple)):
        new = obj.__class__(change_keys(v, convert) for v in obj)
    else:
        return obj
    return new

def replace_dot(string):
    newstring = string.replace(".", "-")
    return newstring


with open(path) as f:

    with app.app_context():
         entries = mongo.db.entries
         for parsed_json in load_json_multiple(f):
             newjson = change_keys(parsed_json, replace_dot)
             entries.update_one(
                 {"id": newjson["id"]},
                 {"$setOnInsert": newjson},
                 upsert=True,
             )





if __name__ == '__main__':
    app.run()