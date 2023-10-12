from flask import Flask, jsonify, request
from flask_cors import CORS
import os

app = Flask(__name__)


@app.route("/")
def ping():
    return jsonify({"message": "API Proyecto 3"})


@app.route("/init")
def init():
    config = os.path.join("DB", "config.xml")
    config = os.path.join("DB", "config.xml")
    config = os.path.join("DB", "config.xml")


if __name__ == "__main__":
    app.run(debug=True, port=3020)
