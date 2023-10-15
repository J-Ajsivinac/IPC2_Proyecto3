from flask import Flask, jsonify, request
from flask_cors import CORS
from read import Read
from builders import *
from controller import Controller
import os

app = Flask(__name__)
CORS(app)
build = Config()
dict_conf = build.config


@app.route("/")
def ping():
    return jsonify({"message": "API Proyecto 3"})


messages = []
r_1 = Read()
r_1.load_initial_data(dict_conf)
r_1.load_initial_msgs(messages)


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


@app.route("/devolverHastags", methods=["POST"])
def get_hastags():
    start = request.json["start"]
    end = request.json["end"]
    ctrl = Controller()
    response = ctrl.filter_hashtag(start, end, messages)
    # print(response)
    return jsonify(response)


@app.route("/devolverMenciones", methods=["POST"])
def get_users():
    start = request.json["start"]
    end = request.json["end"]
    ctrl = Controller()
    response = ctrl.filter_users(start, end, messages)
    return jsonify(response)


@app.route("/test")
def test():
    for msg in messages:
        print(msg.users)
    return {"message": "test"}


if __name__ == "__main__":
    app.run(debug=True, port=3020)
