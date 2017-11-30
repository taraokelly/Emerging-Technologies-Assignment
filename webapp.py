from flask import Flask, request, redirect, url_for, send_from_directory,jsonify
from base64 import decodebytes

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
        print(image)
        # Adapted from: https://stackoverflow.com/questions/35896868/how-to-get-string-after-last-comma-in-a-field
        # Set data to everything after the comma, removing the additional data like "data:image/png;base64".
        data = image.rsplit(',', 1)[1]
        # Adapted from: https://www.mkyong.com/python/python-3-convert-string-to-bytes/
        # Encode string to byte array.
        data = str.encode(data)

        # Save image.
        with open('uploads/'+'imageFileName.png', "wb") as fh:
            fh.write(decodebytes(data))
    #return "image received"
    return jsonify(
        digit="5",
        error=""
    )

if __name__ == "__main__":
    app.run()