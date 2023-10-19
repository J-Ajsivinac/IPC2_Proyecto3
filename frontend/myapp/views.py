from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.http import require_POST
import requests


# Create your views here.
def index(request):
    exito = request.GET.get("exito", None)
    # Convierte exito en un valor booleano
    exito = exito == "True" if exito is not None else None
    return render(request, "index.html", {"exito": exito})


def process_configure(request):
    exito = None
    if request.method == "POST" and request.FILES["archivo"]:
        archivo = request.FILES["archivo"]
        contenido = archivo.read()
        # print(contenido)
        api_url = "http://127.0.0.1:3020/grabarConfiguracion"
        response = requests.post(api_url, data=contenido)
        exito = response.status_code == 200
        # request.session["exito"] = exito
        return redirect(f"/?exito={exito}")
    # exito = request.session.get("exito", None)
    return redirect(f"/?exito={exito}")
