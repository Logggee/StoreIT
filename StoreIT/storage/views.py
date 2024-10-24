from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, JsonResponse
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

def storage_single_item(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
    # Build JSON data for prefilling search master data form 
    data = {
        "item_name": item.item_name,
        "item_image": item.item_image,
        "item_node": item.item_node,
        "item_datasheet": item.item_datasheet,
        "item_purshase_place": item.item_purchase_place
    }
    return JsonResponse(data)

def store_new_item(request):
    if request.method == "POST":
        item_name = request.POST.get('item_name')
        item_quantity = request.POST.get('item_quantity')
        item_volume = request.POST.get('item_volume')
        item_image = request.FILES.get('item_image')  # Für Dateien (Bilder)

        # Neues Item in der Datenbank speichern
        new_item = Item(
            name=item_name,
            quantity=item_quantity,
            volume=item_volume,
            image=item_image
        )
        new_item.save()
    return render(request, 'storage/storage.html')

def config(request):
    return render(request, "storage/configStorage.html")

def stats(request):
    return render(request, "storage/stats.html")