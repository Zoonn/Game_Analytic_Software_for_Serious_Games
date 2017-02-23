from flask import Flask, render_template, request, redirect, flash
from flask_pymongo import PyMongo
from werkzeug.utils import secure_filename
import config
import json
import os


app = Flask(__name__)
app.secret_key = config.secret_key

cwd = os.getcwd()
UPLOAD_FOLDER = cwd + '\JSONs'
ALLOWED_EXTENSIONS = config.allowed_extensions

app.config['MONGO_DBNAME'] = config.mongouser
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
                print(newjson)
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


@app.route('/')
def index():
    return render_template('home.html')


if __name__ == "__main__":
    app.run()
