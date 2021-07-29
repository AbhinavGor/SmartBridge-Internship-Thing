import numpy as np
import os
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import tensorflow as tf
import pickle
from flask import Flask, request, render_template
from werkzeug.utils import secure_filename
from gevent.pywsgi import WSGIServer

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

        # print(request.form["comment"])
        comment_text = request.form["comment"]
        book_name = request.form["book_name"]
        print(book_name, comment_text)
        # print(model.predict(cv.transform(['i did not like this book. Not good. Poor . Waste of time'])))
        # print(model.predict(cv.transform([comment_text])))
        prediction = model.predict(cv.transform([comment_text]))
        if round(prediction[0][0]) == 0:
            #     print("positive review!")
            # else:
            #     print("negative review!")
            return render_template("positive_result.html")

        return render_template("negative_result.html")
    #     # f = request.files['image']
    #     # print("current path")
    #     # basepath = os.path.dirname(__file__)
    #     # print("current path", basepath)
    #     # filepath = os.path.join(basepath, 'uploads', f.filename)
    #     # print("upload folder is ", filepath)
    #     # f.save(filepath)

    #     # img = image.load_img(filepath, target_size=(64, 64))
    #     # x = image.img_to_array(img)
    #     # x = np.expand_dims(x, axis=0)
    #     # x = "Great book loved it!"
    #     f = request.files['comment']
    #     print(f)
    #     preds = model.predict(x)

    #     print("prediction", preds)

    #     index = ['Bear', 'Crow', 'Elephant', 'Racoon', 'Rat']

    #     print(np.argmax(preds))

    #     text = "The animal is a.... : " + str(index[np.argmax(preds)])+" !"
    # return text


if __name__ == '__main__':
    app.run(host="localhost", port=8000, debug=True, threaded=False)
