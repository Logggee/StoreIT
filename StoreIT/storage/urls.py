from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),    # The name can be used for url command in a html href
    path("storage/", views.storage, name="storage")
]