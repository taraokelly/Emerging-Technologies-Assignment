from flask import Flask, request, redirect, url_for, send_from_directory,jsonify
from base64 import decodebytes
import base64
import tensorflow as tf
import numpy as np
import re
import io
from PIL import Image

# Specify uploads directory.
UPLOAD_FOLDER = './uploads'

# Start and configure application.
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Routing: @app.route is a decorator used to match URLs to view functions in Flask apps.
# Root web address - and only web address in this case
@app.route("/")
def root():
    return app.send_static_file('index.html')

# GET/POST methods
@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        image = request.values["image"]
        # Adapted from: https://stackoverflow.com/questions/35896868/how-to-get-string-after-last-comma-in-a-field
        # Set data to everything after the comma, removing the additional data like "data:image/png;base64".
        data = image.rsplit(',', 1)[1]
        # Adapted from: https://www.mkyong.com/python/python-3-convert-string-to-bytes/
        # Encode string to byte array.
        data = str.encode(data)
        #print(data)
        #print(type(data))

        # Save image.
        with open('uploads/'+'imageFileName.png', "wb") as fh:
            fh.write(decodebytes(data))

        # https://www.reddit.com/r/learnpython/comments/6lqsrp/converting_a_dataurl_to_numpy_array/
        imgstr = re.search(r'base64,(.*)', image).group(1)
        image_bytes = io.BytesIO(base64.b64decode(imgstr))
        im = Image.open(image_bytes)
        def normalize(x):
            # https://stackoverflow.com/questions/10848990/rgb-values-to-0-to-1-scale
            # I noticed the white pixel's in the mnist dataset images never had the value of 1 so I used 256 instead of 255 
            return x / 256
        
        # numpy's vectorize function to vectorize the function - specified the output result as float32
        normalize = np.vectorize(normalize, otypes=[np.float32]) 
        # call this normalize function and pass in the pixel data from the bytes decoded from the dataURL
        arr = normalize(np.array(im, dtype=np.float32)[:,:,0])
        # flatten from 2d to 1d and convert to list
        arr = arr.flatten().tolist()
        print(arr)
    return jsonify(
        digit="5",
        error=""
    )

if __name__ == "__main__":
    app.run()