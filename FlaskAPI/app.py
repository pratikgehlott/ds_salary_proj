# -*- coding: utf-8 -*-
"""
Created on Wed Oct 28 07:38:24 2020

@author: Gehlot Pratik
"""
import flask
from flask import Flask, jsonify, request
import json
import pickle
import numpy as np
from data_input import data_in
def load_models():
    file_name = "models/model_file.p"
    with open(file_name, 'rb') as pickled:
        data = pickle.load(pickled)
        model = data['model']
    return model

app = Flask(__name__)
@app.route('/predict', methods=['GET'])
def predict():  
    # stub input features
    # x = np.array(data_in).reshape(1,-1)
    # parse input features from request
    request_json = request.get_json()
    print(request_json)
    x = request_json['input']
    x_in = np.array(list(x)).reshape(1,-1)
    # load model
    model = load_models()
    prediction = model.predict(x_in)[0]
    response = json.dumps({'response': prediction})
    return response, 200


if __name__ == '__main__':
    application.run(debug=True)