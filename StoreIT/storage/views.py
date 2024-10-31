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

        content = {"total_stored_quantity_per_item": Stored_Item.get_total_stored_quantity_for_all_items(), # Gets a list with the summed up stored quantity of each item that is stored any where
                   "items_list": Item.objects.all(), 
                   "store_item_form": Store_Item_Form(),
                   "destore_item_form": Destore_Item_Form(),
                   "new_stored_item": new_stored_item,
                   "storage_page_state": storage_page_state.name}
        storage_page_state = Storage_Page_State.INIT
        return render(request, "storage/storage.html", content)
    
def store_existing_item (request, item_id):
    ''' storage/store_existing_item/<int:item_id>
    This url endpoint is used to store a item where the same item is already stored somewhere.
    So only the quantity in the storage space needs to be updated. The function pics the same
    Bin where the other same items are already stored.
    Note that after the redirect the modal for the sotage process is opend right away.

    Args:
        request: HTTP request object
        item_id: primary key of a Item relation

    Returns:
        A redirect to the url /storage/storage
    '''
    global storage_page_state
    if request.method == "POST":
        # Get all same stored items
        stored_items = Stored_Item.objects.filter(item_id=item_id)
        #TODO Algo for searching for the last bin where same item was stored to add this item
        print(stored_items)

        storage_page_state = Storage_Page_State.STORE_ITEM_PROCESS
        return redirect("storage:storage")

def stored_single_item(request, item_id):
    ''' /storage/<int:item_id>
    This url endpoint is used to get a single item via a ajax call. The items
    attributes are displayed in the add item form to prefill all fields when
    one in selected via a checkbox.

    Args:
        request: HTTP request object

    Returns:
        A JSON object with all item attributes of a single item
    '''
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
            stored_item = get_object_or_404(Stored_Item, item_id=stored_item_fk)
            # Safe the delta quantity
            stored_item.stored_item_quantity = stored_item.stored_item_quantity - destore_quantity
            # If no quantity is left at this storage place the dataset can be deleted
            if stored_item.stored_item_quantity == 0:
                stored_item.delete()
            else:
                stored_item.save()
            storage_page_state = Storage_Page_State.DESTORE_ITEM_PROCESS
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
    return render(request, "storage/configStorage.html")

def stats(request):
    ''' /stats
    Stats page

    Args:
        request: HTTP request object

    Returns:
        Renders the template stats.html
    '''
    return render(request, "storage/stats.html")