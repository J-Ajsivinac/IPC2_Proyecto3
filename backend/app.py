from flask import Flask, jsonify, request
from flask_cors import CORS
from read import Read
from builders import *
from controller import Controller
import os
import copy


class MainBackend:
    def __init__(self):
        self.build = Config()
        self.dict_conf = self.build.config
        self.messages = []
        self.load_initial_data()

    def reset_data(self):
        self.dict_conf = self.build.reset()
        self.messages.clear()

    def load_initial_data(self):
        r_1 = Read()
        r_1.load_initial_data(self.dict_conf)
        r_1.load_initial_msgs(self.messages)


origin_data = MainBackend()

app = Flask(__name__)
CORS(app)


@app.route("/")
def ping():
    return jsonify({"message": "API Proyecto 3"})


@app.route("/grabarConfiguracion", methods=["POST"])
def charge():
    xml_data = request.data
    r_ = Read()
    dict_conf = origin_data.dict_conf
    build = origin_data.build
    r_.read_config(xml_data, dict_conf, build)
    print("Valor actualizado de clave1:", dict_conf["sentimientos_positivos"])
    print("Valor actualizado de clave2:", dict_conf["sentimientos_negativos"])
    return {"mensaje": "XML procesado correctamente"}


@app.route("/grabarMensajes", methods=["POST"])
def charge_msg():
    xml_data = request.data
    dict_conf = origin_data.dict_conf
    messages = origin_data.messages
    r_ = Read()
    r_.load_msg(xml_data, dict_conf, messages)
    # return {"mensaje": "XML procesado correctamente", "valores": messages}
    response = copy.deepcopy(messages)
    serial = [obj.__dict__ for obj in response]

    return jsonify(serial)


@app.route("/devolverHastags", methods=["POST"])
def get_hastags():
    start = request.json["start"]
    end = request.json["end"]
    messages = origin_data.messages
    ctrl = Controller()
    response = ctrl.filter_hashtag(start, end, messages)
    # print(response)
    return jsonify(response)


@app.route("/devolverMenciones", methods=["POST"])
def get_users():
    start = request.json["start"]
    end = request.json["end"]
    messages = origin_data.messages
    ctrl = Controller()
    response = ctrl.filter_users(start, end, messages)
    return jsonify(response)


@app.route("/devolverSentimientos", methods=["POST"])
def get_sentiments():
    start = request.json["start"]
    end = request.json["end"]
    messages = origin_data.messages
    ctrl = Controller()
    response = ctrl.filter_sentiments(start, end, messages)
    return jsonify(response)


@app.route("/limpiarDatos")
def restet():
    origin_data.reset_data()
    r_ = Read()
    r_.restet_db()
    return {"mensaje": "Sistema inicializado"}


@app.route("/test")
def test():
    for msg in origin_data.messages:
        print(msg.users)
    return {"message": "test"}


if __name__ == "__main__":
    app.run(debug=True, port=3020)
