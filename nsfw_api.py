# python3
import os
import pickle
import cherrypy
from paste.translogger import TransLogger
from flask import Flask, request, abort, jsonify, make_response
import scipy as sp
import numpy as np
import sys
import argparse
import glob
import time
from PIL import Image
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO
from nsfw_detector import NSFWDetector
import tensorflow as tf


# app
app = Flask(__name__)
BAD_REQUEST = 400
STATUS_OK = 200
NOT_FOUND = 404
SERVER_ERROR = 500


@app.errorhandler(BAD_REQUEST)
def bad_request(error):
    return make_response(jsonify({'error': 'Bad request'}), BAD_REQUEST)


@app.errorhandler(NOT_FOUND)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), NOT_FOUND)


@app.errorhandler(SERVER_ERROR)
def server_error(error):
    return make_response(jsonify({'error': 'Server Internal Error'}), SERVER_ERROR)


def run_server():
    # Enable WSGI access logging via Paste
    app_logged = TransLogger(app)

    # Mount the WSGI callable object (app) on the root directory
    cherrypy.tree.graft(app_logged, '/')

    # Set the configuration of the web server
    cherrypy.config.update({
        'engine.autoreload_on': True,
        'log.screen': True,
        'log.access_file': 'access.log',
        'log.error_file': 'cherrypy.log',
        'server.socket_port': 5000,
        'server.socket_host': '0.0.0.0',
        'server.thread_pool': 50,  # 10 is default
    })

    # Start the CherryPy WSGI web server
    cherrypy.engine.start()
    cherrypy.engine.block()


def classify_nsfw(filename):
    print('filename:', filename)
    global graph
    with graph.as_default():
        scores = detector.predict(filename)
    print('scores:', scores)
    for k, v in scores.items():
        nsfw_score = float(v['sexy'] + v['porn'] + v['hentai'])
    return nsfw_score


@app.route('/')
def index():
    return 'Yeah, yeah, I highly recommend it'


@app.route('/nsfw', methods=['POST'])
def nsfw():
    if not request.is_json:
        abort(BAD_REQUEST)
    dict_query = request.get_json()
    if 'filename' not in dict_query:
        abort(BAD_REQUEST)

    filename = dict_query['filename']
    score = classify_nsfw(filename)
    result = dict()
    result['score'] = score
    return make_response(jsonify(result), STATUS_OK)


detector = NSFWDetector('./nsfw.299x299.h5')
graph = tf.get_default_graph()  # refer to: https://github.com/keras-team/keras/issues/2397


if __name__ == '__main__':
    run_server()
