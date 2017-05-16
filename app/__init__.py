import json
import os

from bson import json_util
from flask import Flask, render_template, request, redirect, flash
from flask_pymongo import PyMongo
from werkzeug.utils import secure_filename
from collections import defaultdict

import config



app = Flask(__name__)
app.config.from_object('config')
app.secret_key = config.secret_key


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.',1)[1] in config.ALLOWED_EXTENSIONS


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


@app.route('/upload', methods=['GET', 'POST'])
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
            path = config.basedir + '/app/JSONs'
            file.save(os.path.join(path, filename))

            result = []
            newjsonpath = path + '/' +filename
            oldjsonpath = path + '/' + 'jsons.json'

            with open(newjsonpath) as newjson_file:
                with open(oldjsonpath) as oldjson_file:
                    for parsed_json in load_json_multiple(oldjson_file):
                        result.append(parsed_json)
                    for parsed_json in load_json_multiple(newjson_file):
                        newjson = change_keys(parsed_json, replace_dot)
                        result.append(newjson)

            with open(oldjsonpath, "w") as outfile:
                for new in result:
                    json.dump(new, outfile)
                    outfile.write('\n')

            os.remove(newjsonpath)
            flash(filename + ": Upload successful!")

            # newpath = config.UPLOAD_FOLDER + "/"+filename
            # init_db(newpath)
            #flash(filename + ": Upload into database successful!")
            return redirect(request.url)
        else:
            flash("No supported file")

    return render_template('upload.html')


def toJson(data):
    return json.dumps(data, default=json_util.default, sort_keys=True, indent=4, separators=(',', ': ')
                      , ensure_ascii=False)


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('home.html')


@app.route('/fetch', methods=['GET'])
def get_all_entries():
    jsonpath = config.UPLOAD_FOLDER + '/jsons.json'
    json_results = []
    json_keys = []
    with open(jsonpath) as results:
        for result in results:
            jsons = json.loads(result)
            json_results.append(jsons)
            keys = jsons.keys()
            for key in keys:
                if key not in json_keys:
                    json_keys.append(key)
    return render_template("json.html", json=toJson(json_results), names=json_keys)


@app.route('/delete_entries')
def delete_entries():
    json_path = config.UPLOAD_FOLDER + '/jsons.json'
    with open(json_path, "w"):
        pass

    flash('Removal successful!')

    return render_template("home.html")


@app.route('/entries/<json_id>', methods=['GET'])
def get_entry(json_id):
    jsonpath = config.UPLOAD_FOLDER + '/jsons.json'
    results = []
    id_results = {}
    parsed_dict = {}
    with open(jsonpath) as results:
        for result in results:
            jsons = json.loads(result)
            keys = jsons.keys()
         #   for k, v in jsons:
           #     if k in id_results:
          #          id_results[k].append(v)
           #     else:
            #        var = result
           #         id_results[k] = v


    return toJson(id_results)


def myprint(d):
    dicts = {}
    for k, v in d.items():
        if isinstance(v, dict):
            myprint(v)
        else:
             dicts[k] = v

    return dicts


@app.route('/help')
def help():
    return render_template('help.html')


@app.route('/chartpage')
def chartpage():
    return render_template('chartpage.html')

@app.route('/charttest')
def charttest(chartID = 'chart_ID', chart_type = 'bar', chart_height = 350):
    chart = {"renderTo": chartID, "type": chart_type, "height": chart_height,}
    series = [{"name": 'Label1', "data": [1,2,3]}, {"name": 'Label2', "data": [4, 5, 6]}]
    title = {"text": 'My Title'}
    xAxis = {"categories": ['xAxis Data1', 'xAxis Data2', 'xAxis Data3']}
    yAxis = {"title": {"text": 'yAxis Label'}}
    return render_template('chartTest.html', chartID=chartID, chart=chart, series=series, title=title, xAxis=xAxis, yAxis=yAxis)


def parse_json(json_results):
    parsed_jsons = defaultdict(list)

    for key, value in json_results:
        parsed_jsons[key].append(value)

    d = dict((key, tuple(value)) for key, value in parsed_jsons.items())

    print(d)

