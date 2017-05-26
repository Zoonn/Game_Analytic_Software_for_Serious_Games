import json
import os

from bson import json_util
from flask import Flask, render_template, request, redirect, flash
from werkzeug.utils import secure_filename


import config

app = Flask(__name__)
app.config.from_object('config')
app.secret_key = config.secret_key


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in config.ALLOWED_EXTENSIONS


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
            newjsonpath = path + '/' + filename
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

            return redirect(request.url)
        else:
            flash("No supported file")

    return render_template('upload.html')


def toJson(data):
    return json.dumps(data, default=json_util.default, sort_keys=True, indent=4, separators=(',', ': ')
                      )


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('home.html')


@app.route('/fetch', methods=['GET'])
def get_all_entries():
    jsonpath = config.UPLOAD_FOLDER + '/jsons.json'
    json_results = []
    key_dict = {}
    json_keys = []
    nestedkeylist = []
    secondnestedkeylist = []
    with open(jsonpath) as results:
        for result in results:
            jsons = json.loads(result)
            json_results.append(jsons)
            keys = jsons.keys()

            for key in keys:
                if key not in json_keys:
                    json_keys.append(key)

            for key in jsons:
                value = jsons[key]
                if isinstance(value, dict):
                    nestedkeys = value.keys()

                    for key2 in nestedkeys:
                        if key2 not in nestedkeylist:
                            nestedkeylist.append(key2)

                    key_dict[key] = nestedkeylist

                    for key3 in value:
                        secondvalue = value[key3]
                        if isinstance(secondvalue, dict):
                            secondnestedkeys = secondvalue.keys()

                            for key4 in secondnestedkeys:
                                if key4 not in json_keys:
                                    secondnestedkeylist.append(key4)
                            key_dict[key] = secondnestedkeylist

    return render_template("json.html", json=toJson(json_results), names=json_keys, keydict=key_dict)


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
    id_results = {}

    with open(jsonpath) as results:
        for result in results:
            jsons = json.loads(result)
            for key in jsons:
                value = jsons[key]
                if isinstance(value, dict):
                    for secondkey in value:
                        secondvalue = value[secondkey]

                        if isinstance(secondvalue, dict):
                            for thirdkey in secondvalue:
                                thirdvalue = secondvalue[thirdkey]

                                if isinstance(thirdvalue, dict):
                                    for fourthkey in thirdvalue:
                                        fourthvalue = thirdvalue[fourthkey]

                                        if isinstance(fourthvalue, dict):
                                            for fifthkey in fourthvalue:
                                                fifthvalue = fourthvalue[fifthkey]

                                                if isinstance(fifthvalue, dict):
                                                    for sixthkey in fifthvalue:
                                                        sixthvalue = fifthvalue[sixthkey]

                                                        if sixthkey == json_id:
                                                            if sixthvalue in id_results:
                                                                id_results[sixthvalue] += 1
                                                            else:
                                                                id_results[sixthvalue] = 1

                                                else:
                                                    if fifthkey == json_id:
                                                        if fifthvalue in id_results:
                                                            id_results[fifthvalue] += 1
                                                        else:
                                                            id_results[fifthvalue] = 1
                                        else:
                                            if fourthkey == json_id:
                                                if fourthvalue in id_results:
                                                    id_results[fourthvalue] += 1
                                                else:
                                                    id_results[fourthvalue] = 1
                                else:
                                    if thirdkey == json_id:
                                        if thirdvalue in id_results:
                                            id_results[thirdvalue] += 1
                                        else:
                                            id_results[thirdvalue] = 1
                        elif secondkey == json_id:
                            if secondkey == json_id:
                                if secondvalue in id_results:
                                    id_results[secondvalue] += 1
                                else:
                                    id_results[secondvalue] = 1

                else:
                    if key == json_id:
                        if value in id_results:
                            id_results[value] += 1
                        else:
                            id_results[value] = 1

    return toJson(id_results)


@app.route('/chartpage')
def chartpage():
    return render_template('chartpage.html')



