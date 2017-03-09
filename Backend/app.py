

from flask import Flask, render_template, request, redirect, flash, jsonify
from flask_pymongo import PyMongo
from werkzeug.utils import secure_filename
from bson import json_util
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


@app.route('/fetch', methods=['GET'])
def get_all_entries():
    entry = mongo.db.entries
    lim = int(request.args.get('limit', 200))
    off = int(request.args.get('offset', 0))
    results = entry.find().skip(off).limit(lim)
    json_results = []
    json_keys = []
    key = 0
    for result in results:
        json_results.append(result)
        keys = result.keys()
        for key in keys:
            if key not in json_keys:
                json_keys.append(key)
    return render_template("json.html", json=toJson(json_results), names=json_keys)


@app.route('/delete_entries')
def delete_entries():
    entry = mongo.db.entries
    entry.drop()
    flash("Dropped collection")
    return render_template("home.html")


@app.route('/entries', methods=['GET'])
def get_entries():
    entry = mongo.db.entries
    lim = int(request.args.get('limit', 200))
    off = int(request.args.get('offset', 0))
    results = entry.find().skip(off).limit(lim)
    json_results = []

    for result in results:
        json_results.append(result)

    return toJson(json_results)


@app.route('/entries/<json_id>', methods=['GET'])
def get_entry(json_id):
    entry = mongo.db.entries

    results = entry.find({ },{json_id : 1, "_id" :0})
    json_results = []

    for result in results:
        json_results.append(result)

    return toJson(json_results)


@app.route('/entries/num', methods=['GET'])
def get_entry_num():

    results = mongo.db.entries.aggregate([
        {"$match": {
                "keywords": {"$not": {"$size": 0}}
            }
        },
        { "$unwind": "$keywords"},
        {
        "$group": {
            "_id": {"$toLower": '$keywords'},
        "count": { "$sum": 1}
        }
        },
        {
        "$match": {
            "count": { "$gte": 2}
        }
        },
        { "$sort": {"count": -1}},
        { "$limit": 100}
     ])

    return results['result']

@app.route('/graph')
def graph(chartID='chart_id', chart_type='line', chart_height=500):
    chart = {"renderTo": chartID, "type": chart_type, "height": chart_height, }
    series = [{"name": 'Label1', "data": [1, 2, 3]}, {"name": 'Label2', "data": [4, 5, 6]}]
    title = {"text": 'My Title'}
    xAxis = {"categories": ['xAxis Data1', 'xAxis Data2', 'xAxis Data3']}
    yAxis = {"title": {"text": 'yAxis Label'}}
    return render_template('home.html', chartID=chartID, chart=chart, series=series, title=title, xAxis=xAxis,
                           yAxis=yAxis)


if __name__ == "__main__":
    app.run()
