from flask import Flask, jsonify, request
from flask_cors import CORS
from read import Read
from builders import *
from writeResume import Write
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
    response = origin_data.load_config(xml_data)
    return {"mensaje": "XML procesado correctamente", "data": response}


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


@app.route("/limpiarDatos")
def restet():
    origin_data.reset_data()
    return {"mensaje": "Sistema inicializado"}


@app.route("/SalidaMensajes", methods=["POST"])
def create_msg():
    req = request.json["root"]
    root = os.path.join(req, "resumenMensajes.xml")
    write = Write()
    write.write_resume(root, origin_data.messages)
    return {"mensaje": "Archivo grabado exitosamente"}


@app.route("/SalidaSentimientos", methods=["POST"])
def create_sentiments():
    req = request.json["root"]
    root = os.path.join(req, "resumenConfig.xml")
    write = Write()
    # test.xml
    write.write_resume_confif(root, origin_data.dict_conf)
    return {"mensaje": "Archivo grabado exitosamente"}


if __name__ == "__main__":
    app.run(debug=True, port=3020)
