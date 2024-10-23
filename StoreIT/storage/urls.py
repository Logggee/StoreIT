from django.urls import path
from . import views

urlpatterns = [
    # localhost:8000
    path("", views.index, name="index"),    # The name can be used for url command in a html href
    # localhost:8000/storage/
    path("storage/", views.storage, name="storage"),
    # localhost:8000/config/
    path("config/", views.config, name="config"),
    # localhost:8000/stats
    path("stats/", views.stats, name="stats")
]