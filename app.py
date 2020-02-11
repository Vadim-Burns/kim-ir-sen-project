from flask import Flask
import os

app = Flask(__name__)


@app.route('/')
def hello_world():
    return os.environ("security_key")


if __name__ == '__main__':
    app.run()
