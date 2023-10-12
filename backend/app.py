from flask import Flask, jsonify, request
from flask_cors import CORS
from read import Read
from builders import *
import os

app = Flask(__name__)
build = Config()
dict_conf = build.config


@app.route("/")
def ping():
    return jsonify({"message": "API Proyecto 3"})


r_1 = Read()
r_1.load_initial_data(dict_conf)


@app.route("/init_db", methods=["POST"])
def init():
    # xml_data = request.data
    # r_ = Read()
    # r_.write_file(dict_conf, build)
    return {"mensaje": "XML procesado correctamente"}


@app.route("/grabarConfiguracion", methods=["POST"])
def charge():
    xml_data = request.data
    r_ = Read()
    r_.read_config(xml_data, dict_conf, build)
    print("Valor actualizado de clave1:", dict_conf["sentimientos_positivos"])
    print("Valor actualizado de clave2:", dict_conf["sentimientos_negativos"])
    return {"mensaje": "XML procesado correctamente"}


if __name__ == "__main__":
    app.run(debug=True, port=3020)
