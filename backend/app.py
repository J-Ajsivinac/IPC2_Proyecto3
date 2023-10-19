from flask import Flask, jsonify, request
from flask_cors import CORS
from read import Read
from builders import *
from controller import Controller
import os
import copy

read = Read()
origin_data = MainBackend(read)

app = Flask(__name__)
CORS(app)


@app.route("/")
def ping():
    return jsonify({"message": "API Proyecto 3"})


@app.route("/grabarConfiguracion", methods=["POST"])
def charge():
    xml_data = request.data
    origin_data.load_config(xml_data)
    return {"mensaje": "XML procesado correctamente"}


@app.route("/grabarMensajes", methods=["POST"])
def charge_msg():
    xml_data = request.data
    origin_data.load_messages(xml_data)
    return {"message": "Archivo grabado exitosamente"}


@app.route("/devolverHastags", methods=["POST"])
def get_hastags():
    start = request.json["start"]
    end = request.json["end"]
    response = origin_data.return_hashtags(start, end)
    return jsonify(response)


@app.route("/devolverMenciones", methods=["POST"])
def get_users():
    start = request.json["start"]
    end = request.json["end"]
    response = origin_data.return_users(start, end)
    return jsonify(response)


@app.route("/devolverSentimientos", methods=["POST"])
def get_sentiments():
    start = request.json["start"]
    end = request.json["end"]
    response = origin_data.return_sentiments(start, end)
    return jsonify(response)


@app.route("/devolverGraficaSentimientos", methods=["POST"])
def get_graph_sentiments():
    start = request.json["start"]
    end = request.json["end"]
    response = origin_data.return_sentiments(start, end)
    return jsonify(response)


@app.route("/devolverGraficaHashtags", methods=["POST"])
def get_graph_hash():
    start = request.json["start"]
    end = request.json["end"]
    response = origin_data.return_graph_hash(start, end)
    return jsonify(response)


@app.route("/devolverGraficaUsuarios", methods=["POST"])
def get_graph_users():
    start = request.json["start"]
    end = request.json["end"]
    response = origin_data.return_graph_u(start, end)
    return jsonify(response)


@app.route("/limpiarDatos")
def restet():
    origin_data.reset_data()
    return {"mensaje": "Sistema inicializado"}


@app.route("/test")
def test():
    for msg in origin_data.messages:
        print(msg.users)
    return {"message": "test"}


if __name__ == "__main__":
    app.run(debug=True, port=3020)
