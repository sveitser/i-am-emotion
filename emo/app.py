#!/usr/bin/env python
import json
import os

from flask import Flask, flash, request, redirect, url_for, jsonify
import tensorflow as tf
import numpy as np

import sys

import cv2
from keras.models import load_model
import numpy as np

from utils.datasets import get_labels
from utils.inference import detect_faces
from utils.inference import draw_text
from utils.inference import draw_bounding_box
from utils.inference import apply_offsets
from utils.inference import load_detection_model
from utils.inference import load_image
from utils.preprocessor import preprocess_input
#from predict import predict_emotion_gender, extract_face

# parameters for loading data and images
detection_model_path = 'trained_models/detection_models/haarcascade_frontalface_default.xml'
emotion_model_path = 'trained_models/emotion_models/fer2013_mini_XCEPTION.102-0.66.hdf5'
gender_model_path = 'trained_models/gender_models/simple_CNN.81-0.96.hdf5'
emotion_labels = get_labels('fer2013')
gender_labels = get_labels('imdb')

# hyper-parameters for bounding boxes shape
gender_offsets = (30, 60)
gender_offsets = (10, 10)
emotion_offsets = (20, 40)
emotion_offsets = (0, 0)

# loading models
face_detection = load_detection_model(detection_model_path)
emotion_classifier = load_model(emotion_model_path, compile=False)
gender_classifier = load_model(gender_model_path, compile=False)

graph = tf.get_default_graph()

# getting input model shapes for inference
emotion_target_size = emotion_classifier.input_shape[1:3]
gender_target_size = gender_classifier.input_shape[1:3]


def predict_emotion_gender(rgb_face, gray_face):

    rgb_face = preprocess_input(rgb_face, False)
    rgb_face = np.expand_dims(rgb_face, 0)
    gender_prediction = gender_classifier.predict(rgb_face)
    gender_label_arg = np.argmax(gender_prediction)
    gender_text = gender_labels[gender_label_arg]

    gray_face = preprocess_input(gray_face, True)
    gray_face = np.expand_dims(gray_face, 0)
    gray_face = np.expand_dims(gray_face, -1)
    emotion_label_arg = np.argmax(emotion_classifier.predict(gray_face))
    emotion_text = emotion_labels[emotion_label_arg]
    #emotion_text = 'None'

    return (emotion_text, gender_text)

def extract_face(rgb_image, gray_image, face_coordinates):
    x1, x2, y1, y2 = apply_offsets(face_coordinates, gender_offsets)
    rgb_face = rgb_image[y1:y2, x1:x2]

    x1, x2, y1, y2 = apply_offsets(face_coordinates, emotion_offsets)
    gray_face = gray_image[y1:y2, x1:x2]

    try:
        rgb_face = cv2.resize(rgb_face, (gender_target_size))
        gray_face = cv2.resize(gray_face, (emotion_target_size))
    except:
        return None, None

    return rgb_face, gray_face

def create_context(labels):
    # context = f"I am a {' '.join(labels)}."
    context = labels
    return context

app = Flask(__name__)

@app.route("/", methods=['POST'])
def predict():

    print('received image', request)
    imagefile = request.files.get('image', '')
    npimg = np.fromfile(imagefile, 'uint8')
    rgb_image = cv2.imdecode(npimg, cv2.IMREAD_COLOR) #load_image(image_path, grayscale=False)
    gray_image = cv2.imdecode(npimg, cv2.IMREAD_GRAYSCALE) #load_image(image_path, grayscale=True)
    gray_image = np.squeeze(gray_image)
    gray_image = gray_image.astype('uint8')
    #print(rgb_image.shape)

    try:
        face_coordinates = detect_faces(face_detection, gray_image)
        #print(face_coordinates)
        global graph
        with graph.as_default():
            rgb_face, gray_face = extract_face(rgb_image, gray_image, face_coordinates)
            label = predict_emotion_gender(rgb_face, gray_face)
            context = create_context(label)

        # if label[1] == gender_labels[0]:
        #     color = (0, 0, 255)
        # else:
        #     color = (255, 0, 0)

        # draw_bounding_box(face_coordinates, rgb_image, color)
        # draw_text(face_coordinates, rgb_image, label[1], color, 0, -20, 1, 2)
        # draw_text(face_coordinates, rgb_image, label[0], color, 0, -50, 1, 2)

        # bgr_image = cv2.cvtColor(rgb_image, cv2.COLOR_RGB2BGR)
        # cv2.imwrite('images/1face.png', bgr_image)

        return jsonify(context)

    except Exception as e:
        #print(e)
        return jsonify(['happy', 'woman'])

def main():
    app.run(host="0.0.0.0", debug=True, port=4000)


if __name__ == "__main__":
    main()
