import numpy as np
import os
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import tensorflow as tf
import pickle
from flask import Flask, request, render_template
from werkzeug.utils import secure_filename
from gevent.pywsgi import WSGIServer


import json
from isbntools.app import *
import requests

from urllib.request import urlopen

app = Flask(__name__)
model = load_model("model.h5")
cv_saved = cv = pickle.load(open('cv.pkl', 'rb'))


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/another_review')
def comeback():
    return render_template('index.html')


@app.route('/predict', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':

        comment_text = request.form["comment"]
        book_name = request.form["book_name"]

        api = "https://www.googleapis.com/books/v1/volumes?q=isbn:"

        ISBN = isbn_from_words(book_name)

        resp = urlopen(api + ISBN)
        book_data = json.load(resp)
        try:
            image_link = book_data['items'][0]['volumeInfo']['imageLinks']['thumbnail']
        except KeyError:
            return render_template("error.html")
        prediction = model.predict(cv.transform([comment_text]))
        if round(prediction[0][0]) == 0:
            return render_template("positive_result.html", link=image_link)
        return render_template("negative_result.html", link=image_link)


if __name__ == '__main__':
    app.run(host="localhost", port=8000, debug=True, threaded=False)
