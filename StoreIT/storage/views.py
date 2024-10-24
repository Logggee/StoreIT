import os
from django.conf import settings
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.http import Http404
from django.core.files.storage import default_storage
from .models import Stored_Item, Item
from .forms import Store_Item_Form

def index(request):
    return render(request, "storage/index.html")

def storage(request):
    stored_items_list = Stored_Item.objects.all()
    items_list = Item.objects.all()
    store_item_form = Store_Item_Form()
    content = {"stored_items_list": stored_items_list, "items_list": items_list, "store_item_form": store_item_form}
    return render(request, "storage/storage.html", content)

def storage_single_item(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
    # Build JSON data for prefilling search master data form 
    data = {
        "item_id": item.item_id,
        "item_name": item.item_name,
        "item_image": item.item_image,
        "item_node": item.item_node,
        "item_datasheet": item.item_datasheet,
        "item_purchase_place": item.item_purchase_place
    }
    return JsonResponse(data)

def store_new_item(request):
    if request.method == "POST":
        post_item_name = request.POST.get('item_name')
        post_item_quantity = request.POST.get('item_quantity')
        post_item_volume = request.POST.get('item_volume')
        post_item_image = request.FILES.get('item_image_file')
        post_item_node = request.POST.get('item_node')
        post_item_datasheet = request.POST.get('item_datasheet')
        post_item_purchase_place = request.POST.get('item_puchase_place')

        # Safe the items image
        item_image_directory = os.path.join(settings.BASE_DIR, 'storage/static/storage/images/item_images')
        # If the folder does not exist create one
        if not os.path.exists(item_image_directory):
            os.makedirs(item_image_directory)

        item_file_name = post_item_image.name
        item_image_file_path = os.path.join(item_image_directory, item_file_name)


        print(f"File Path: {item_image_file_path}")

        with default_storage.open(item_image_file_path, 'wb+') as destination:
            for chunk in post_item_image.chunks():
                destination.write(chunk)

        # Add new item to the database
        new_item = Item(
            item_name = post_item_name,
            item_quantity = post_item_quantity,
            item_volume = post_item_volume,
            item_image = item_file_name,
            item_node = post_item_node,
            item_datasheet = post_item_datasheet,
            item_purchase_place = post_item_purchase_place
        )
        new_item.save()
    return render(request, 'storage/storage.html')

def config(request):
    return render(request, "storage/configStorage.html")

def stats(request):
    return render(request, "storage/stats.html")