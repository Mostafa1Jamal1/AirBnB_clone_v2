#!/usr/bin/python3
''' a script that starts a Flask web application '''

from flask import Flask

app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello():
    ''' display “Hello HBNB!” on route / '''
    return "Hello HBNB!"


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    ''' display “HBNB” on route /hbnb '''
    return "HBNB"


@app.route('/c/<text>', strict_slashes=False)
def cisfun(text):
    ''' display “C” followed by the value of the text
    and replace _ with space on route /c/<text> '''
    return f"C {text.replace('_', ' ')}"


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
