# TODO: 防注入攻击

from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/search-result.html', methods=['GET'])
def search_result():
    word = request.values.get('word')
    return render_template('search-result.html', word=word)


if __name__ == '__main__':
    app.run(debug=True)
