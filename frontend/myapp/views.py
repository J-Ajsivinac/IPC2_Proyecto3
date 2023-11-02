from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_POST
from django.urls import reverse
import requests
import json
import os
import xml.etree.ElementTree as ET


# Create your views here.
def index(request):
    if request.method == "GET":
        if request.GET.get("reset") is not None:
            exito = None
            try:
                api_url = "http://127.0.0.1:3020/limpiarDatos"
                response = requests.get(api_url, timeout=100)
                response_api = response.json()
                exito = response.status_code == 200
            except Exception as _:
                exito = False
            if exito:
                return render(
                    request,
                    "index.html",
                    {
                        "reset": exito,
                        "type_r": response_api["type_r"],
                        "message": response_api["msg"],
                    },
                )
            else:
                return render(
                    request,
                    "index.html",
                    {
                        "reset": exito,
                        "type_r": 0,
                        "message": "Error al conectar con el servidor",
                    },
                )
        exito = request.GET.get("exito", None)
        exito = exito == "True" if exito is not None else None
        return render(request, "index.html", {"exito": exito, "data": ""})
    elif request.method == "POST":
        # cargar diccionario de  configuraciones
        if "file-1" in request.FILES:
            exito = None
            response_api = None
            try:
                archivo = request.FILES["file-1"]
                contenido = archivo.read()
                api_url = "http://127.0.0.1:3020/grabarConfiguracion"
                response = requests.post(api_url, data=contenido, timeout=300)
                response_api = response.json()
                exito = response.status_code == 200
                if exito:
                    current_directory = os.path.dirname(__file__)
                    parent_directory = os.path.dirname(current_directory)
                    project_directory = os.path.dirname(parent_directory)
                    desired_directory = os.path.join(project_directory, "resumenes")
                    if not os.path.exists(desired_directory):
                        os.makedirs(desired_directory)
                    save = os.path.join(desired_directory, "resumenConfig.xml")
                    # root = ET.fromstring(str(response_api["data"]))
                    with open(save, "w", encoding="utf-8") as f:
                        f.write(str(response_api["data"]))
                    return render(
                        request,
                        "index.html",
                        {
                            "exito": exito,
                            "data": str(response_api["data"]),
                        },
                    )
                else:
                    return render(
                        request,
                        "index.html",
                        {
                            "exito": exito,
                            "data": "",
                        },
                    )
            except Exception as _:
                exito = False
                return render(
                    request,
                    "index.html",
                    {
                        "exito": exito,
                        "data": "",
                    },
                )

        # cargar mensajes para analizar
        elif "file-2" in request.FILES:
            exito = None
            try:
                archivo = request.FILES["file-2"]
                contenido = archivo.read()
                api_url = "http://127.0.0.1:3020/grabarMensajes"
                response = requests.post(api_url, data=contenido, timeout=1000)
                response_api = response.json()
                exito = response.status_code == 200
                if exito:
                    current_directory = os.path.dirname(__file__)
                    parent_directory = os.path.dirname(current_directory)
                    project_directory = os.path.dirname(parent_directory)
                    desired_directory = os.path.join(project_directory, "resumenes")
                    if not os.path.exists(desired_directory):
                        os.makedirs(desired_directory)
                    save = os.path.join(desired_directory, "resumenMensajes.xml")
                    # root = ET.fromstring(str(response_api["data"]))
                    with open(save, "w", encoding="utf-8") as f:
                        f.write(str(response_api["data"]))
                    return render(
                        request,
                        "index.html",
                        {
                            "exito": exito,
                            "data": str(response_api["data"]),
                        },
                    )
                return render(
                    request,
                    "index.html",
                    {
                        "exito": exito,
                        "data": "",
                    },
                )
            except Exception as _:
                exito = False
                return render(
                    request,
                    "index.html",
                    {
                        "exito": exito,
                        "data": "",
                    },
                )
    exito = request.GET.get("exito", None)
    exito = exito == "True" if exito is not None else None
    return render(request, "index.html", {"exito": exito})


def search(request):
    if request.method == "GET":
        return render(request, "search.html")
    elif request.method == "POST":
        response = None
        if "rangeDate" in request.POST:
            search_by = request.POST["searchBy"]
            range_date = request.POST["rangeDate"]
            range_date = range_date.split("-")
            if len(range_date) != 2 or len(range_date) == 0:
                return render(
                    request,
                    "search.html",
                    {
                        "data": None,
                        "type_r": 2,
                        "message": "No se selecciono un rango de fechas adecuado",
                    },
                )
            start = range_date[0].strip()
            end = range_date[1].strip()
            api_url = ""
            try:
                if search_by == "hashtags":
                    api_url = "http://127.0.0.1:3020/devolverHashtags"
                elif search_by == "mentions":
                    api_url = "http://127.0.0.1:3020/devolverMenciones"
                elif search_by == "sentiments":
                    api_url = "http://127.0.0.1:3020/devolverSentimientos"
                data = {"start": start, "end": end}
                data_json = json.dumps(data)
                headers = {"Content-Type": "application/json"}
                response = requests.post(
                    api_url, headers=headers, data=data_json, timeout=1000
                )
                response_api = response.json()
                graph_data = {"data_graph": response_api["data_graph"]}
                graph_data = json.dumps(graph_data)
                if response.status_code == 200:
                    return render(
                        request,
                        "search.html",
                        {
                            "data": response_api["data"],
                            "type_r": response_api["type_r"],
                            "graph_data": graph_data,
                            "message": response_api["message"],
                        },
                    )
                else:
                    return render(
                        request,
                        "search.html",
                        {
                            "data": "None",
                            "type_r": 2,
                            "message": "Error al conectar con el sevidor",
                        },
                    )
            except Exception as _:
                return render(
                    request,
                    "search.html",
                    {
                        "data": "None",
                        "type_r": 2,
                        "message": "Error al conectar con el servidor",
                    },
                )
        else:
            return render(
                request,
                "search.html",
                {
                    "data": None,
                    "type_r": 2,
                    "message": "Ocurrio un error con las fechas <br> vuelva a intetarlo",
                },
            )


def help_p(request):
    return render(request, "help.html")
