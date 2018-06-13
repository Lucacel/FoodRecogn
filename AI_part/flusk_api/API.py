import io
import os
import flask
import numpy as np
from PIL import Image
from keras.models import load_model
from keras.preprocessing.image import img_to_array
import sqlite3

DATA_BASE_PATH = 'D:\Projects\\0FoodRecogn\AI_part\\flusk_api\\food_recogn.db'
MODEL_PATH = 'D:\\Projects\\0FoodRecogn\\AI_part\\flusk_api\\FoodRecognModel.h5'
CLASSES_PATH = 'D:\Projects\\0FoodRecogn\AI_part\\flusk_api\\resources\classes.txt'

app = flask.Flask(__name__)
model = None


def loadmodel():
    global model
    model = load_model(filepath=MODEL_PATH)


def get_classes():
    with open(CLASSES_PATH, 'r') as x_txt:
        x_classes = [l.strip() for l in x_txt.readlines()]
        x_ix_to_class = dict(zip(range(len(x_classes)), x_classes))
        x_class_to_ix = {v: k for k, v in x_ix_to_class.items()}
    return x_class_to_ix


def preprocess_input(x):
    x /= 255.
    x -= 0.5
    x *= 2
    return x


def prepare_image(image, target):
    # if img is not RGB, convert it
    if image.mode != "RGB":
        image = image.convert("RGB")

    image = image.resize(target)
    image = img_to_array(image)
    image = np.expand_dims(image, axis=0)
    image = preprocess_input(image)
    # image = imagenet_utils.preprocess_input(image)

    return image


def top__preds(preds):
    top_preds = []
    for i in range(0, 100):
        if (preds[0][i] <= 1) and (preds[0][i] > 0):
            top_preds.append(i)
    return top_preds


@app.route("/predict", methods=["POST"])
def predict():
    data = {"success": False}

    if flask.request.method == "POST":
        if flask.request.files.get("image"):
            image = flask.request.files["image"].read()
            image = Image.open(io.BytesIO(image))

            image = prepare_image(image, target=(299, 299))

            preds = model.predict(image, 32, 1)
            preds = preds.tolist()
            t_preds = top__preds(preds)
            classes = get_classes()

            result = []

            for t in t_preds:
                for i in classes:
                    if classes[i] == t:
                        if preds[0][t] * 100 > 30:
                            result.append(str(i + " " + str(preds[0][t] * 100)))

            data["predictions"] = []

            if not result:
                data["predictions"].append("I don't really know")
            else:
                for r in result:
                    print(r + '\n')
                    data["predictions"].append(r)

            data["success"] = True

    return flask.jsonify(data)


@app.route("/")
def index():
    return flask.render_template("Index.html")


@app.route("/login", methods=["POST"])
def login_function():
    data = {"login": True}
    content = flask.request.get_json(silent=True)
    print(content)
    return flask.jsonify(data)


if __name__ == '__main__':
    print("Server is starting ...")
    loadmodel()
    print("Server started: ...")
    app.run(port=8086)
