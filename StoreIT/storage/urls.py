from django.urls import path
from . import views

app_name = "storage"

urlpatterns = [
    # localhost:8000
    path("", views.index, name="index"),    # The name can be used for url command in a html href
    # localhost:8000/storage/
    path("storage/", views.storage, name="storage"),
    # localhost:8000/storage/1
    path("storage/<int:item_id>", views.storage_single_item, name="storage_single_item"),
    # localhost:8000/storage/store_item
    path("storage/store_new_item", views.store_new_item, name="store_new_item"),
    # localhost:8000/config/
    path("config/", views.config, name="config"),
    # localhost:8000/stats
    path("stats/", views.stats, name="stats")
]