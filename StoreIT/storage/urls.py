from django.urls import path
from . import views
from .views import User_Login

app_name = "storage"

urlpatterns = [
    # localhost:8000
    path("", views.index, name="index"),    # The name can be used for url command in a html href
    # localhost:8000/storage/
    # This url is also used to post a new item to the db
    path("storage/", views.storage, name="storage"),
    # localhost:8000/storage/1
    path("storage/<int:item_id>", views.stored_single_item, name="stored_single_item"),
    # localhost:8000/storage/store_existing_item_1
    # Caution this is used by the same form as /storage the action url is set in storage.js if the user
    # selected a item from the master data list via a checkbox
    path("storage/store_existing_item/<int:item_id>", views.store_existing_item, name="store_existing_item"),
    # localhost:8000/storage/destore_item/1
    # Url is used to destore a specific quantity of a stored item
    path("storage/destore_item/<int:stored_item_fk>", views.destore_item, name="destore_item"),
    # localhost:8000/storage/confirm_storing/<int:reservation_id>
    path("storage/confirm_storing/<int:reservation_id>", views.confirm_storing, name="confirm_storing"),
    # localhost:8000/storage/cancel_storing/<int:reservation_id>
    path("storage/cancel_storing/<int:reservation_id>", views.cancel_storing, name="cancel_storing"),
    # localhost:8000/storage/confirm_destoring/<int:reservation_id>
    path("storage/confirm_destoring/<int:reservation_id>", views.confirm_destoring, name="confirm_destoring"),
    # localhost:8000/storage/cancel_destoring/<int:reservation_id>
    path("storage/cancel_destoring/<int:reservation_id>", views.cancel_destoring, name="cancel_destoring"),
    # localhost:8000/config/
    path("config/", views.config, name="config"),
    # localhost:8000/1/12
    path("config/<int:bin_id>", views.all_items_stored_in_bin, name="all_items_stored_in_bin"),
    # localhost:8000/stats
    path("stats/", views.stats, name="stats"),
    # localhost:8000/accounts/login
    path('accounts/login/', User_Login.as_view(), name='login'),
    # localhost:8000/accounts/login
    path('register/', views.register, name='register'),
]