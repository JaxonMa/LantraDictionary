#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask, render_template, jsonify
from flask_cors import CORS

import dictionary

app = Flask(__name__)
CORS(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/search-results')
def search_results():
    return render_template('search-results.html')


@app.route('/lookup/<query>', methods=['GET'])
def lookup(query):
    query_res = dictionary.lookup(query)
    return jsonify(query_res)


if __name__ == '__main__':
    app.run(debug=True)
