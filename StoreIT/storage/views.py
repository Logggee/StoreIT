# views.py
import os
from django.conf import settings
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.http import Http404
from django.core.files.storage import default_storage
from .models import Stored_Item, Item, Bin
from .forms import Store_Item_Form, Destore_Item_Form
from .utils import Storage_Page_State

# Enum that holds the current state of the /storage template
# The states define which modals are opend initially
storage_page_state = Storage_Page_State.INIT

''' /
Landingpage

Params:
    request: HTTP request object

Returns:
    Renders the template index.html
'''
def index(request):
    return render(request, "storage/index.html")

def storage(request):
    global storage_page_state
    # Post request
    if request.method == "POST":
        # Validate the form and parse the POST data
        store_item_form = Store_Item_Form(request.POST, request.FILES)
        if store_item_form.is_valid():
            # Safe the items image
            item_image_directory = os.path.join(settings.BASE_DIR, 'storage/static/storage/images/item_images')
            # If the folder does not exist create one
            if not os.path.exists(item_image_directory):
                os.makedirs(item_image_directory)

            item_file_name = store_item_form.cleaned_data["item_image_file"].name
            item_image_file_path = os.path.join(item_image_directory, item_file_name)
            # Safe the image
            with default_storage.open(item_image_file_path, 'wb+') as destination:
                for chunk in store_item_form.cleaned_data["item_image_file"].chunks():
                    destination.write(chunk)

            new_item = Item(item_name = store_item_form.cleaned_data["item_name"],
                            item_image = store_item_form.cleaned_data["item_image_file"].name,
                            item_node = store_item_form.cleaned_data["item_node"],
                            item_datasheet = store_item_form.cleaned_data["item_datasheet"],
                            item_purchase_place = store_item_form.cleaned_data["item_purchase_place"])
            new_item.save()

            # Add a new stored item to the database
            # TODO Storage algorythm goes here
            new_stored_item = Stored_Item (bin_id = Bin.objects.get(pk = 1),
                                           item_id = new_item,
                                           stored_item_quantity = store_item_form.cleaned_data["item_quantity"])
            new_stored_item.save()
            # Safe the name and quantity of the item to display it in the modal after the redirect
            request.session["new_stored_item"] = (store_item_form.cleaned_data["item_name"], store_item_form.cleaned_data["item_quantity"])
            storage_page_state = Storage_Page_State.STORE_PROCESS

            return redirect("storage:storage")
        
        # Form was not valid
        else:
            stored_items_list = Stored_Item.objects.all()
            items_list = Item.objects.all()
            storage_page_state = Storage_Page_State.ADD_ITEM_FORM_ERROR
            destore_item_form = Destore_Item_Form()
            content = {"stored_items_list": stored_items_list,
                       "items_list": items_list,
                       "store_item_form": store_item_form,
                       "destore_item_form": destore_item_form,
                       "storage_page_state": storage_page_state.name} # Variable that declares to open the modal after reload
            storage_page_state = Storage_Page_State.INIT
            return render(request, "storage/storage.html", content)
        
    # Get request
    else:
        new_stored_item = request.session.pop("new_stored_item", False)

        stored_items_list = Stored_Item.objects.all()
        items_list = Item.objects.all()
        store_item_form = Store_Item_Form()
        destore_item_form = Destore_Item_Form()
        content = {"stored_items_list": stored_items_list, 
                   "items_list": items_list, 
                   "store_item_form": store_item_form,
                   "destore_item_form": destore_item_form,
                   "new_stored_item": new_stored_item,
                   "storage_page_state": storage_page_state.name}
        storage_page_state = Storage_Page_State.INIT
        return render(request, "storage/storage.html", content)
    
''' storage/store_existing_item/<int:item_id>

This url endpoint is used to store a item where the same item is already stored somewhere.
So only the quantity in the storage space needs to be updated. The function pics the same
Bin where the other same items are already stored.
Note that after the redirect the modal for the sotage process is opend right away.

Params:
    request: HTTP request object
    item_id: primary key of a Item relation

Returns:
    A redirect to the url /storage/storage
'''
def store_existing_item (request, item_id):
    global storage_page_state
    if request.method == "POST":
        # Get all same stored items
        stored_items = Stored_Item.objects.filter(item_id=item_id)
        #TODO Algo for searching for the last bin where same item was stored to add this item
        print(stored_items)

        storage_page_state = Storage_Page_State.STORE_PROCESS
        return redirect("storage:storage")

''' /storage/<int:item_id>
This url endpoint is used to get a single item via a ajax call. The items
attributes are displayed in the add item form to prefill all fields when
one in selected via a checkbox.

Params:
    request: HTTP request object

Returns:
    A JSON object with all item attributes of a single item
'''
def stored_single_item(request, item_id):
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

def destore_item(request, stored_item_fk):
    if request.method == "POST":
        destore_item_form = Destore_Item_Form(request.POST, stored_item_fk=stored_item_fk)

        if destore_item_form.is_valid():
            return redirect("storage:storage")
        
        # Form was not valid
        else:
            print("Form was not valid")
            stored_items_list = Stored_Item.objects.all()
            items_list = Item.objects.all()
            storage_page_state = Storage_Page_State.DESTORE_ITEM_FORM_ERROR
            content = {"stored_items_list": stored_items_list,
                       "items_list": items_list,
                       "destore_item_form": destore_item_form,
                       "stored_item_form_error": get_object_or_404(Stored_Item, item_id=stored_item_fk), # Used to open the correct modal where the error happend
                       "storage_page_state": storage_page_state.name} # Variable that declares to open the modal after reload
            storage_page_state = Storage_Page_State.INIT
            return render(request, "storage/storage.html", content)

''' /config
Config page

Params:
    request: HTTP request object

Returns:
    Renders the template config.html
'''
def config(request):
    return render(request, "storage/configStorage.html")

''' /stats
Stats page

Params:
    request: HTTP request object

Returns:
    Renders the template stats.html
'''
def stats(request):
    return render(request, "storage/stats.html")