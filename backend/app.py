from flask import Flask, jsonify, request
from flask_cors import CORS
from read import Read
from builders import *
import os

app = Flask(__name__)
CORS(app)
build = Config()
dict_conf = build.config


@app.route("/")
def ping():
    return jsonify({"message": "API Proyecto 3"})


r_1 = Read()
r_1.load_initial_data(dict_conf)
messages = []


@app.route("/grabarConfiguracion", methods=["POST"])
def charge():
    xml_data = request.data
    r_ = Read()
    r_.read_config(xml_data, dict_conf, build)
    print("Valor actualizado de clave1:", dict_conf["sentimientos_positivos"])
    print("Valor actualizado de clave2:", dict_conf["sentimientos_negativos"])
    return {"mensaje": "XML procesado correctamente"}


@app.route("/grabarMensajes", methods=["POST"])
def charge_msg():
    xml_data = request.data
    r_ = Read()
    r_.load_msg(xml_data, dict_conf, messages)
    # return {"mensaje": "XML procesado correctamente", "valores": messages}
    serial = [obj.__dict__ for obj in messages]

    return jsonify(serial)


if __name__ == "__main__":
    app.run(debug=True, port=3020)
