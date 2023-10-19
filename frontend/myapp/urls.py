from django.urls import path
from . import views

urlpatterns = [
    path("", views.index),
    path("/", views.index),
    path("cargar-archivo/", views.process_configure, name="process_configure"),
]
