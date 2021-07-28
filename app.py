import numpy as np
import os
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import tensorflow as tf

from flask import Flask, request, render_template
from werkzeug.utils import secure_filename
from gevent.pywsgi import WSGIServer

app = Flask(__name__)
model = load_model("model.h5")


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/predict', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        f = request.files['image']
        print("current path")
        basepath = os.path.dirname(__file__)
        print("current path", basepath)
        filepath = os.path.join(basepath, 'uploads', f.filename)
        print("upload folder is ", filepath)
        f.save(filepath)

        img = image.load_img(filepath, target_size=(64, 64))
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        preds = model.predict(x)

        print("prediction", preds)

        index = ['Bear', 'Crow', 'Elephant', 'Racoon', 'Rat']

        print(np.argmax(preds))

        text = "The animal is a.... : " + str(index[np.argmax(preds)])+" !"
    return text


if __name__ == '__main__':
    #app.run(debug = True, threaded = False)
    #app.run(debug = True,threaded = False ,host='127.0.0.2', port=5002)
    app.run(host="localhost", port=8000, debug=True, threaded=False)
