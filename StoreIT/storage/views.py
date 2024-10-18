from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from django.template import loader
from django.http import Http404

def index(request):
    return render(request, "storage/index.html")

def storage(request):
    return render(request, "storage/storage.html")

def config(request):
    return render(request, "storage/configStorage.html")

def stats(request):
    return render(request, "storage/stats.html")