#!/usr/bin/python3.5
from flask import Flask
app = Flask(__name__)
@app.route("/")
def hello():
    return "Hello Gunicorn"

if __name__ == "__main__":
    from werkzeug.contrib.fixers import ProxyFix
    app.wsgi_app = ProxyFix(app.wsgi_app)
    app.run()
