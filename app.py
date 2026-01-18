#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# TODO: 防注入攻击

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS

import dictionary

app = Flask(__name__)
CORS(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/search', methods=['GET'])
def search():
    word = request.values.get('word')
    return render_template('search-results.html')


@app.route('/api/lookup/<query>', methods=['POST'])
def lookup(query):
    query_res = dictionary.lookup(query, 'chinese')
    return jsonify(query_res)


if __name__ == '__main__':
    app.run(debug=True)
