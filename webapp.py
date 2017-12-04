from flask import Flask, request, redirect, url_for, send_from_directory,jsonify
import tensorflow as tf
import numpy as np
import re, io, base64,os, model,pandas,subprocess
from PIL import Image

# Specify configuration variables.
IMAGE_SIZE = 28
MODEL_DIR = '/model/'
MODEL_NAME = 'model'
MODEL_EXT = ['.index', '.data-00000-of-00001']
# Current working dir - for tf 
CWD =  os.getcwd().replace("\\","/")
FILEPATH = CWD + MODEL_DIR + MODEL_NAME

for ext in MODEL_EXT:
    if not os.path.isfile(FILEPATH + ext) :
        model.create(FILEPATH)
        break

# Reset so that the variables generated (only if the model had just been created that is) don't interfere with resoring the graph.
tf.reset_default_graph()

sess = tf.Session()

x = tf.placeholder(tf.float32, shape=[None, 784])
y_ = tf.placeholder(tf.float32, shape=[None, 10])

y_conv, keep_prob = model.setup(x)
# then restore
saver = tf.train.Saver()
saver.restore(sess, FILEPATH)

# Start application.
app = Flask(__name__)

# Routing: @app.route is a decorator used to match URLs to view functions in Flask apps.
# Root web address - and only web address in this case
@app.route("/")
def root():
    return app.send_static_file('index.html')

# GET/POST methods
@app.route('/model', methods=['GET','POST'])
def model():
    if request.method == 'POST':
        image = request.values["image"]
        prepared_image = prepare(image)
        prediction,score = "",""
        # make prediction on array and make serializable for JSON
        prediction = pandas.Series(predict(prepared_image)).to_json(orient='values')
        return jsonify(
            accuracy = score,
            digit = prediction,
        )

def prepare(image):
    # https://www.reddit.com/r/learnpython/comments/6lqsrp/converting_a_dataurl_to_numpy_array/
    imgstr = re.search(r'base64,(.*)', image).group(1)
    image_bytes = io.BytesIO(base64.b64decode(imgstr))
    im = Image.open(image_bytes)
    # Image.ANTIALIAS minimises distortion when representing a high-resolution image at a lower resolution
    im = im.resize((IMAGE_SIZE, IMAGE_SIZE), Image.ANTIALIAS)
    def normalize(x):
        # https://stackoverflow.com/questions/10848990/rgb-values-to-0-to-1-scale
        # I noticed the white pixel's in the mnist dataset images never had the value of 1 so I used 256 instead of 255 
        return x / 256
    # https://stackoverflow.com/questions/7701429/efficient-evaluation-of-a-function-at-every-cell-of-a-numpy-array
    # numpy's vectorize function to vectorize the function - specifies the output result as float32
    normalize = np.vectorize(normalize, otypes=[np.float32]) 
    # call this normalize function and pass in the pixel data from the bytes decoded from the dataURL
    arr = normalize(np.array(im, dtype=np.float32)[:,:,0])
    # flatten from 2d to 1d and convert to list
    return arr.flatten().tolist()

def predict(input):
    # Returns the index with the largest value across axes of a tensor.
    # So will return 0-9 since we have 10 classifications.
    return sess.run(tf.argmax(y_conv, 1), feed_dict={x: [input], keep_prob: 1.0})

if __name__ == "__main__":
    app.run()