from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from django.template import loader
from django.http import Http404
from .models import Stored_Item, Item

def index(request):
    return render(request, "storage/index.html")

def storage(request):
    stored_items_list = Stored_Item.objects.all()
    items_list = Item.objects.all()
    content = {"stored_items_list": stored_items_list, "items_list": items_list}
    return render(request, "storage/storage.html", content)

def config(request):
    return render(request, "storage/configStorage.html")

def stats(request):
    return render(request, "storage/stats.html")