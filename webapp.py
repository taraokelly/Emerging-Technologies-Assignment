import os
from flask import Flask, request, redirect, url_for
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = '/uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/")
def root():
    return app.send_static_file('index.html')

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    return "file uploaded"

if __name__ == "__main__":
    app.run()