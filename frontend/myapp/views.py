from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.urls import reverse
import requests


# Create your views here.
def index(request):
    if request.method == "GET":
        exito = request.GET.get("exito")
        return render(request, "index.html", {"exito": exito})
    elif request.method == "POST" and request.FILES["archivo"]:
        exito = None
        try:
            archivo = request.FILES["archivo"]
            contenido = archivo.read()
            api_url = "http://127.0.0.1:3020/grabarConfiguracion"
            response = requests.post(api_url, data=contenido, timeout=100)
            exito = response.status_code == 200
        except Exception as _:
            exito = False

        # request.method = "GET"
        return redirect(f"{reverse('index')}?exito={exito}")
    exito = request.GET.get("exito")
    return render(request, "index.html", {"exito": exito})
