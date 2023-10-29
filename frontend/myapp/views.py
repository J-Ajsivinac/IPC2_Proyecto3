from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_POST
from django.urls import reverse
import requests
import json


# Create your views here.
def index(request):
    if request.method == "GET":
        if request.GET.get("reset") is not None:
            exito = None
            try:
                api_url = "http://127.0.0.1:3020/limpiarDatos"
                response = requests.get(api_url, timeout=100)
                exito = response.status_code == 200
                print(exito)
            except Exception as _:
                exito = False
                print(exito, "---")
            return redirect(f"{reverse('index')}?exito={exito}")
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
                # print(contenido)
                api_url = "http://127.0.0.1:3020/grabarConfiguracion"
                response = requests.post(api_url, data=contenido, timeout=100)
                response_api = response.json()
                # print(response_api["data"])
                exito = response.status_code == 200
                return render(
                    request,
                    "index.html",
                    {
                        "exito": exito,
                        "data": str(response_api["data"]),
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
            # print("entro en config")
            try:
                archivo = request.FILES["file-2"]
                contenido = archivo.read()
                api_url = "http://127.0.0.1:3020/grabarMensajes"
                response = requests.post(api_url, data=contenido, timeout=1000)
                exito = response.status_code == 200
            except Exception as _:
                exito = False

            return redirect(f"{reverse('index')}?exito={exito}")
        # return redirect(f"{reverse('index')}?exito={exito}")
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
            if len(range_date) != 2:
                # print(range_date, "error")
                return redirect(reverse("search"))
            start = range_date[0].strip()
            end = range_date[1].strip()
            api_url = ""
            try:
                if search_by == "hashtags":
                    api_url = "http://127.0.0.1:3020/devolverHastags"
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
                # graph_data = json.dumps(response_api["data_graph"])
                graph_data = {"data_graph": response_api["data_graph"]}
                graph_data = json.dumps(graph_data)
                if response.status_code == 200:
                    # print(data)
                    return render(
                        request,
                        "search.html",
                        {
                            "data": response_api["data"],
                            "type_r": response_api["type_r"],
                            "graph_data": graph_data,
                        },
                    )
                else:
                    # print("error")
                    return render(
                        request,
                        "search.html",
                        {"data": "None", "type_r": 0},
                    )
            except Exception as _:
                return render(
                    request,
                    "search.html",
                    {"data": "None", "type_r": 0},
                )
        else:
            # print("error")
            return render(
                request,
                "search.html",
                {"data": None, "type_r": 2},
            )


def help_p(request):
    return render(request, "help.html")


# def test(request):
#     graph_data = {"data_graph": {"bienvenidaUSAC": "4", "saludoUSAC": "2"}}
#     print(json.dumps(graph_data))
#     return render(request, "graph.html", {"graph_data": json.dumps(graph_data)})
