from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.urls import reverse
import requests


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
        return render(request, "index.html", {"exito": exito})
    elif request.method == "POST":
        # cargar diccionario de  configuraciones
        if "config" in request.FILES:
            exito = None
            print("entro en config")
            try:
                archivo = request.FILES["config"]
                contenido = archivo.read()
                api_url = "http://127.0.0.1:3020/grabarConfiguracion"
                response = requests.post(api_url, data=contenido, timeout=100)
                exito = response.status_code == 200
            except Exception as _:
                exito = False

            # request.method = "GET"
            return redirect(f"{reverse('index')}?exito={exito}")
        # cargar mensajes para analizar
        elif "msgs" in request.FILES:
            exito = None
            print("entro en config")
            try:
                archivo = request.FILES["msgs"]
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
    return render(request, "search.html")
