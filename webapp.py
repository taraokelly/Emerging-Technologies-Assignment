import os
import flask
from flask import Flask, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
import base64
from base64 import decodestring
import re

# Specify uploads directory.
UPLOAD_FOLDER = './uploads'

# We only want to allow images to be uploaded  - so only allowing files with the following extensions.
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

# Start and configure application.
app = flask.Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Routing: @app.route is a decorator used to match URLs to view functions in Flask apps.
# Root web address - and only web address in this case
@app.route("/")
def root():
    return app.send_static_file('index.html')

# this url will be removed
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],filename)

@app.route('/', methods=['GET', 'POST'])
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
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            #return redirect(url_for('uploaded_file',
            #                       filename=filename))
            return redirect(request.url)
    return redirect(request.url)

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        image = request.values["image"]
        print(image)
        # Adapted from: https://stackoverflow.com/questions/35896868/how-to-get-string-after-last-comma-in-a-field
        # Set data to everything after the comma, removing the additional data like "data:image/png;base64".
        data = image.rsplit(',', 1)[1]
        # Adapted from: https://www.mkyong.com/python/python-3-convert-string-to-bytes/
        # Encode string to byte array.
        data = str.encode(data)

        # Save image.
        with open('uploads/'+'imageFileName.png', "wb") as fh:
            fh.write(base64.decodebytes(data))
    return "image received"

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

if __name__ == "__main__":
    app.run()