# views.py
import os
import json
import re
from django.conf import settings
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.http import Http404
from django.core.files.storage import default_storage
from django.core.serializers import serialize
from .models import Stored_Item, Item, Bin, Storage
from .forms import Store_Item_Form, Destore_Item_Form, Storage_Layout_Form
from .utils import Storage_Page_State
from . import storageProcesses as storage_processes

# Enum that holds the current state of the /storage template
# The states define which modals are opend initially
storage_page_state = Storage_Page_State.INIT

def index(request):
    """ /
    Landingpage

    Args:
        request: HTTP request object

    Returns:
        Renders the template index.html
    """
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
            # Build and Safe a new dataset of the new item
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
            storage_page_state = Storage_Page_State.STORE_ITEM_PROCESS

            return redirect("storage:storage")
        
        # Form was not valid
        else:
            storage_page_state = Storage_Page_State.ADD_ITEM_FORM_ERROR
            content = {"total_stored_quantity_per_item": Stored_Item.get_total_stored_quantity_for_all_items(),
                       "items_list": Item.objects.all(),
                       "store_item_form": store_item_form,
                       "destore_item_form": Destore_Item_Form(),
                       "storage_page_state": storage_page_state.name} # Variable that declares to open the modal after reload
            storage_page_state = Storage_Page_State.INIT
            return render(request, "storage/storage.html", content)
        
    # Get request
    else:
        # If there was a redirect from storage POST then get the data which item and quantity was added via the session storage
        new_stored_item = request.session.pop("new_stored_item", False)
        # If a item was destored the session storage holds the destored item. This is needed to fill the destore modal
        destore_places_and_quantitys = request.session.pop("destore_places_and_quantitys", list())
        if len(destore_places_and_quantitys) != 0:
            for destore_place_and_quantity in destore_places_and_quantitys:
                storage = get_object_or_404(Storage, pk=destore_place_and_quantity["destored_storage_id"])
                print(f"Storage {storage}")
                destore_place_and_quantity["destored_storage_layout"] = storage.all_bins_sorted_in_rows()
        print(f"Destore place and quantitys: {destore_places_and_quantitys}")
        content = {"total_stored_quantity_per_item": Stored_Item.get_total_stored_quantity_for_all_items(), # Gets a list with the summed up stored quantity of each item that is stored any where
                   "items_list": Item.objects.all(), 
                   "store_item_form": Store_Item_Form(),
                   "destore_item_form": Destore_Item_Form(),
                   "new_stored_item": new_stored_item,
                   "destore_places_and_quantitys": destore_places_and_quantitys,
                   "storage_page_state": storage_page_state.name}
        storage_page_state = Storage_Page_State.INIT
        return render(request, "storage/storage.html", content)
    
def store_existing_item (request, item_id):
    """ storage/store_existing_item/<int:item_id>
    This url endpoint is used to store a item where the same item is already stored somewhere.
    So only the quantity in the storage space needs to be updated. The function pics the same
    Bin where the other same items are already stored.
    Note that after the redirect the modal for the sotage process is opend right away.

    Args:
        request: HTTP request object
        item_id: primary key of a Item relation

    Returns:
        A redirect to the url /storage/storage
    """
    global storage_page_state
    if request.method == "POST":
        # Get all same stored items
        stored_items = Stored_Item.objects.filter(item_id=item_id)
        #TODO Algo for searching for the last bin where same item was stored to add this item
        print(stored_items)

        storage_page_state = Storage_Page_State.STORE_ITEM_PROCESS
        return redirect("storage:storage")

def stored_single_item(request, item_id):
    """ /storage/<int:item_id>
    This url endpoint is used to get a single item via a ajax call. The items
    attributes are displayed in the add item form to prefill all fields when
    one in selected via a checkbox.

    Args:
        request: HTTP request object

    Returns:
        A JSON object with all item attributes of a single item
    """
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
    ''' /storage/destore_itme/<int:stored_item_fk>
    This url endpoint is used to destore a quantity of a stored item.

    Args:
        request: HTTP request object
        stored_item_fk: The item foregin key of a Stored_Item

    Returns:
        Ether a render if there was a error in the form or
        a redirect if the form was valid.
    '''
    global storage_page_state
    if request.method == "POST":
        destore_item_form = Destore_Item_Form(request.POST, stored_item_fk=stored_item_fk)
        # Form was valid
        if destore_item_form.is_valid():
            destore_quantity = destore_item_form.cleaned_data["item_destore_quantity"]
            # Function that destores the item after the FIFO principle
            # Return holds all the stored items that whare destored and the coresponding quantitys
            destore_places_and_quantitys = storage_processes.destore_item(stored_item_fk, destore_quantity)
            print(f"Destore Places and quantitys: {destore_places_and_quantitys}")
            storage_page_state = Storage_Page_State.DESTORE_ITEM_PROCESS
            # Safe the data in the session storage to show it in the modal/modals after the redirect
            request.session["destore_places_and_quantitys"] = destore_places_and_quantitys
            return redirect("storage:storage")
        
        # Form was not valid
        else:
            storage_page_state = Storage_Page_State.DESTORE_ITEM_FORM_ERROR
            content = {"total_stored_quantity_per_item": Stored_Item.get_total_stored_quantity_for_all_items(),
                       "items_list": Item.objects.all(),
                       "store_item_form": Store_Item_Form(),
                       "destore_item_form": Destore_Item_Form(),
                       "destore_item_form_error": destore_item_form,
                       "item_with_destore_error": get_object_or_404(Item, pk=stored_item_fk), # Used to open the correct modal where the error happend
                       "storage_page_state": storage_page_state.name} # Variable that declares to open the modal after reload
            storage_page_state = Storage_Page_State.INIT
            return render(request, "storage/storage.html", content)

def config(request):
    ''' /config
    Config page

    Args:
        request: HTTP request object

    Returns:
        Renders the template config.html
    '''
    # Post request
    if request.method == "POST":
        form_data = request.POST.dict()
        print(f"Form data: {form_data}")
        # Build and safe a new storage dataset
        new_storage = Storage(storage_name = form_data["storage-name-input"],
                              storage_number_of_rows = int(form_data["storage_rows"]))
        new_storage.save()

        diffrent_number_of_bin_per_row = list()
        diffrent_bin_volumes = list()
        for input_field, field_value in form_data.items():
            # Regex only filters if just a number is after number-of-bins-row-[any number]
            if re.match(r'number-of-bins-row-(\d+)$', input_field):
                # Build a list with all diffrent number of bins per row
                if not field_value in diffrent_number_of_bin_per_row:
                    print(f"Field value: {field_value}")
                    diffrent_number_of_bin_per_row.append(int(field_value))
            # Regex only matches if the string is 'bin-size-' with Capital letters after the last '-'
            elif re.match(r'bin-size-([A-Z]*)$', input_field):
                match = re.match(r'bin-size-([A-Z]*)$', input_field)
                if not field_value in diffrent_bin_volumes:
                    diffrent_bin_volumes.append(int(field_value))
        # Sort least amount of bins per row to most numbers of bins per row
        diffrent_number_of_bin_per_row.sort()
        # Sort biggest volume to smallest volume
        diffrent_bin_volumes.sort(reverse=True)
        # Build a dict where the smallest number of bins matches with the biggest volume and so on for all cobinations
        # Number of bins per row is the key and the coresponding volume is the value
        bin_volumes = dict(zip(diffrent_number_of_bin_per_row, diffrent_bin_volumes))

        # Build the dataset for all the bins of the new storage
        bin_number = 0
        for input_field, field_value in form_data.items():
             match = re.match(r'number-of-bins-row-(\d+)$', input_field)
             # Filter for a row number
             if match:
                # Rows numbers are safed from 0 to n
                row_number = int(match.group(1)) - 1
                # Build all bin datasets for the row
                for col_index in range(int(field_value)):
                    bin_number += 1
                    new_bin = Bin(storage_id = new_storage,
                                  bin_number = bin_number,
                                  bin_row = row_number,
                                  bin_col = col_index,
                                  bin_volume = bin_volumes[int(field_value)],
                                  bin_volume_used = 0)
                    new_bin.save()

        return redirect("storage:config")
    
    # Get request
    else:
        # Get all storages and bins
        # TODO check if list es the better datatype here because the key is maybe not relevant
        storages_and_bins = dict()
        for storage in  Storage.objects.all():
            storages_and_bins[storage] = storage.all_bins_sorted_in_rows()
        print(f"Storaged and all bin: {storages_and_bins}")
        content = {"storage_layout_form": Storage_Layout_Form(),
                   "storages_and_bins": storages_and_bins}
        
        return render(request, "storage/configStorage.html", content)
    
def all_items_stored_in_bin(request, bin_id):
    print("Ajax request")
    all_items_in_bin = Stored_Item.objects.filter(bin_id = bin_id)
    data = {}
    for stored_item in all_items_in_bin:
        data[stored_item.item_id.item_name] = {
            "item_store_date_in_this_bin" : stored_item.stored_item_storedate.strftime("%d.%m.%Y, %H:%M:%S"),
            "item_image": stored_item.item_id.item_image,
            "item_name": stored_item.item_id.item_name,
            "item_quantity_in_this_bin": stored_item.stored_item_quantity
        }
    print(f"All items in bin {all_items_in_bin}")
    data = {"all_items_in_bin": data}
    return JsonResponse(data, safe=False)

def stats(request):
    ''' /stats
    Stats page

    Args:
        request: HTTP request object

    Returns:
        Renders the template stats.html
    '''
    return render(request, "storage/stats.html")