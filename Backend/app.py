from flask import Flask, render_template, request, redirect, flash, jsonify, make_response, url_for
from flask_pymongo import PyMongo
from werkzeug.utils import secure_filename
from bson import json_util
from bson.objectid import ObjectId
import config
import json
import os


app = Flask(__name__)
app.secret_key = config.secret_key

cwd = os.getcwd()
UPLOAD_FOLDER = cwd + '\JSONs'
ALLOWED_EXTENSIONS = config.allowed_extensions

app.config['MONGO_DBNAME'] = config.dbname
app.config['MONGO_URI'] = config.mongouri
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

mongo = PyMongo(app)

path = cwd + "\\JSONs"


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.',1)[1] in config.allowed_extensions


def load_json_multiple(segments):
    chunk = ""

    for segment in segments:
        chunk += segment
        try:
            yield json.loads(chunk)
            chunk = ""
        except ValueError:
            pass


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


def init_db(newpath):
    with open(newpath) as f:
        with app.app_context():
            entries = mongo.db.entries
            for parsed_json in load_json_multiple(f):
                newjson = change_keys(parsed_json, replace_dot)
                entries.update_one(
                     {"id": newjson["id"]},
                     {"$setOnInsert": newjson},
                     upsert=True,
                 )


@app.route('/upload.html', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filename = os.path.splitext(filename)[0] + ".json"
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            flash(filename + ": Upload successful!")
            newpath = path + "\\"+filename
            init_db(newpath)
            flash(filename + ": Upload into database successful!")
            return redirect(request.url)
        else:
            flash("No supported file")

    return render_template('upload.html')


def toJson(data):
    """Convert Mongo object(s) to JSON"""
    return json.dumps(data, default=json_util.default, sort_keys=True, indent=4, separators=(',', ': ')
                      , ensure_ascii=False)


@app.route('/')
def index():
    return render_template('home.html')


@app.route('/json.html', methods=['GET'])
def get_all_entries():
    entry = mongo.db.entries
    lim = int(request.args.get('limit', 100))
    off = int(request.args.get('offset', 0))
    results = entry.find().skip(off).limit(lim)
    json_results = []
    for result in results:
        json_results.append(result)
    return render_template("json.html", json=toJson(json_results))


@app.route('/entries/<username>', methods=['GET'])
def get_one_entry(username):
    entry = mongo.db.entries

    s = entry.find_one({'userName' : username})
    if s:
        output = {'userName' : s['userName'], 'appName' : s['appName']}
    else:
        output = "No such name"
    return jsonify({'result' : output})


@app.route('/entries', methods=['POST'])
def add_entry():
    entry = mongo.db.entries
    name = request.json['userName']
    appName = request.json['appName']
    entry_id = entry.insert({'userName': name, 'appName': appName})
    new_entry = entry.find_one({'_id': entry_id })
    output = {'name' : new_entry['name'], 'appName' : new_entry['appName']}
    return jsonify({'result' : output})


if __name__ == "__main__":
    app.run()
