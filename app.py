#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask, render_template, jsonify

import dictionary

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/search-results')
def search_results():
    return render_template('search-results.html')


@app.route('/lookup/<query>', methods=['GET'])
def lookup(query):
    # 调用dictionary模块的lookup函数进行查询
    uri = 'URI_TO_YOUR_MONGODB_SERVER'  # Replace with your MongoDB URI
    try:
        query_res = dictionary.lookup(query, uri)
        return jsonify(query_res)
    except ValueError as e:
        err_msg = {'error': str(e)}
        return jsonify(err_msg)
    except Exception as e:
        err_msg = {'error': '发生了未知错误'}
        return jsonify(err_msg)


if __name__ == '__main__':
    app.run(debug=True)
