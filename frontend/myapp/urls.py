from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("search/", views.search, name="search"),
    path("help/", views.help_p, name="help"),
    # path("test/", views.test),
]
