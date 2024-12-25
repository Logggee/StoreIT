# storage_view.py

from django.shortcuts import get_object_or_404, render, redirect
from django.http import JsonResponse, HttpResponse
from storage.models import Stored_Item, Item, Bin, Storage, Reservation, Reservated_Storing_Item, Reservated_Destoring_Item
from storage.forms import Store_Item_Form, Destore_Item_Form
from storage.utils import Storage_Page_State
from storage import storageProcesses as storage_processes

# Enum that holds the current state of the /storage template
# The states define which modals are opend initially
storage_page_state = Storage_Page_State.INIT

def storage(request):
    """ /storage/

    Page shows all stored items as cards. There are also modals to add a new item to the storage or
    a modal with a destoring list to destore multiple itmes at once.

    Args:
        request: HTTP request object

    Returns:
        Get: renders the template
        Post: If Post was valid redirect to /storage/ if not valid render template with errors shown
    """
    global storage_page_state
    # Check if a storage even exists if not the add new item button shoud not be displayed
    if len(Storage.objects.all()) > 0:
        storage_exists = True
    else:
        storage_exists = False

    # Post request
    if request.method == "POST":
        # Validate the form and parse the POST data
        store_item_form = Store_Item_Form(request.POST, request.FILES)
        if store_item_form.is_valid():
            storage_processes.store_new_item(request, store_item_form)
            
            # Safe the name and quantity of the item to display it in the modal after the redirect
            request.session["new_stored_item"] = (new_stored_item.stored_item_id, store_item_form.cleaned_data["item_quantity"])
            storage_page_state = Storage_Page_State.STORE_ITEM_PROCESS

            return redirect("storage:storage")
        
        # Form was not valid
        else:
            storage_page_state = Storage_Page_State.ADD_ITEM_FORM_ERROR
            content = {"total_stored_quantity_per_item": Stored_Item.get_total_stored_quantity_for_all_items(),
                       "items_list": Item.objects.all(),
                       "store_item_form": store_item_form,
                       "destore_item_form": Destore_Item_Form(),
                       "storage_page_state": storage_page_state.name, # Variable that declares to open the modal after reload
                       "storage_exists": storage_exists} 
            
            storage_page_state = Storage_Page_State.INIT
            return render(request, "storage/storage.html", content)
        
    # Get request
    else:
        # If there was a redirect from storage POST then get the data which item and quantity was added via the session storage
        new_stored_item_data = request.session.pop("new_stored_item", False)
        new_stored_item = dict()
        print(f"New stored item : {new_stored_item_data}")
        if new_stored_item_data:
            new_stored_item = dict()
            new_stored_item["new_stored_item"] = get_object_or_404(Stored_Item, pk=new_stored_item_data[0])
            new_stored_item["new_stored_item_quantity"] = new_stored_item_data[1]

        # If a item was destored the session storage holds the destored item. This is needed to fill the destore modal
        destore_places_and_quantitys = request.session.pop("destore_places_and_quantitys", list())
        print(f"Session storage: {destore_places_and_quantitys}")
        if len(destore_places_and_quantitys) != 0:
            for destore_place_and_quantity in destore_places_and_quantitys:
                storage = get_object_or_404(Storage, pk=destore_place_and_quantity["destored_storage_id"])
                destore_place_and_quantity["destored_storage_layout"] = storage.all_bins_sorted_in_rows()
        print(destore_places_and_quantitys)

        # If a existing item was stored via the view store_existing_item the session storage holdes the data of the item to be stored
        stored_existing_item = request.session.pop("stored_existing_item", False)
        if stored_existing_item:
            new_existing_stored_item = get_object_or_404(Stored_Item, pk = stored_existing_item["stored_item_id"])
            new_stored_existing_item = {"stored_item": new_existing_stored_item,
                                        "storage_location_layout": new_existing_stored_item.bin_id.storage_id.all_bins_sorted_in_rows(),
                                        "stored_item_quantity": stored_existing_item["stored_item_quantity"],
                                        "reservation_id": stored_existing_item["reservation_id"]}
        else:
            new_stored_existing_item = False

        all_storage_layouts = list()
        # Get the layouts of every Storage
        for storage in Storage.objects.all():
            all_storage_layouts.append((storage, storage.all_bins_sorted_in_rows()))


        content = {"total_stored_quantity_per_item": Stored_Item.get_total_stored_quantity_for_all_items(), # Gets a list with the summed up stored quantity of each item that is stored any where
                   "items_list": Item.objects.all(), 
                   "store_item_form": Store_Item_Form(),
                   "destore_item_form": Destore_Item_Form(),
                   "new_stored_item": new_stored_item,
                   "destore_places_and_quantitys": destore_places_and_quantitys,
                   "storage_page_state": storage_page_state.name,
                   "storage_exists": storage_exists,
                   "all_storage_layouts": all_storage_layouts,
                   "new_stored_existing_item": new_stored_existing_item}
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
    # Check if a storage even exists if not the add new item button shoud not be displayed
    if len(Storage.objects.all()) > 0:
        storage_exists = True
    else:
        storage_exists = False

    if request.method == "POST":
        store_item_form = Store_Item_Form(request.POST, item_image_required=False)        
        if store_item_form.is_valid():
            stored_item, reservation_id = storage_processes.store_existing_item(request, store_item_form, item_id)
            
            request.session["stored_existing_item"] = {"stored_item_id": stored_item.stored_item_id,
                                                       "stored_item_quantity": store_item_form.cleaned_data["item_quantity"],
                                                       "reservation_id": reservation_id}
            storage_page_state = Storage_Page_State.STORE_ITEM_PROCESS
            return redirect("storage:storage")
        else:
            storage_page_state = Storage_Page_State.ADD_EXISTING_ITEM_FORM_ERROR
            print(f"Error item item id: {item_id}")
            print(f"Form was invalid: {store_item_form.errors}")
            content = {"total_stored_quantity_per_item": Stored_Item.get_total_stored_quantity_for_all_items(),
                       "items_list": Item.objects.all(),
                       "store_item_form": store_item_form,
                       "destore_item_form": Destore_Item_Form(),
                       "storage_page_state": storage_page_state.name, # Variable that declares to open the modal after reload
                       "storage_exists": storage_exists,
                       "add_existing_item_error": item_id}
            print(f"Content store_existing_item: {content}")         
            storage_page_state = Storage_Page_State.INIT
            return render(request, "storage/storage.html", content)
        
def destore_item(request, stored_item_id):
    ''' /storage/destore_itme/<int:stored_item_id>
    This url endpoint is used to destore a quantity of a stored item.

    Args:
        request: HTTP request object
        stored_item_id: The item foregin key of a Stored_Item

    Returns:
        Ether a render if there was a error in the form or
        a redirect if the form was valid.
    '''
    global storage_page_state
    if request.method == "POST":
        destore_item_form = Destore_Item_Form(request.POST, stored_item_id=stored_item_id)
        # Form was valid
        if destore_item_form.is_valid():
            # Prevents the user from adding items if no storage exists yet
            if len(Storage.objects.all()) == 0:
                return redirect("storage:storage")
            
            destore_quantity = destore_item_form.cleaned_data["item_destore_quantity"]
            # Function that destores the item after the FIFO principle
            # Return holds all the stored items that whare destored and the coresponding quantitys
            destore_places_and_quantitys = storage_processes.destore_item(request, stored_item_id, destore_quantity)
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
                       "item_with_destore_error": get_object_or_404(Item, pk=stored_item_id), # Used to open the correct modal where the error happend
                       "storage_page_state": storage_page_state.name} # Variable that declares to open the modal after reload
            storage_page_state = Storage_Page_State.INIT
            return render(request, "storage/storage.html", content)
        
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
    if item.item_note == "":
        item_note = "-"
    else:
        item_note = item.item_note
    if item.item_datasheet == "":
        item_datasheet = "-"
    else:
        item_datasheet = item.item_datasheet.url
    if item.item_purchase_place == "":
        item_purchase_place = "-"
    else:
        item_purchase_place = item.item_purchase_place
    # Build JSON data for prefilling search master data form 
    data = {
        "item_id": item.item_id,
        "item_name": item.item_name,
        "item_image": item.item_image.url,
        "item_volume": item.item_volume,
        "item_note": item_note,
        "item_datasheet": item_datasheet,
        "item_purchase_place": item_purchase_place
    }
    return JsonResponse(data)

def confirm_storing(request, reservation_id):
    if request.method == "DELETE":
        # Get the reservation and delete it
        reservation = get_object_or_404(Reservation, pk=reservation_id)
        reservation.delete()
        print("Confirm storing and delete reservation")
        print(f"Reservation with id {reservation_id} is deleted!!!")
        return  HttpResponse("Reservation deleted", status=200)
     
def cancel_storing(request, reservation_id):
    if request.method == "DELETE":
        # Delete the added quantity
        reservated_storing_item = Reservated_Storing_Item.objects.get(reservation_id=reservation_id)
        reservated_storing_item.stored_item_id.stored_item_quantity -= reservated_storing_item.reservated_storing_item_quantity
        # If the quantity is 0 the stored item needs to be removed
        if reservated_storing_item.stored_item_id.stored_item_quantity == 0:
            reservated_storing_item.stored_item_id.delete()
        else:    
            reservated_storing_item.stored_item_id.save()
        # Get the reservation and delete it
        reservation = get_object_or_404(Reservation, pk=reservation_id)
        reservation.delete()
    return  HttpResponse("Reservation deleted", status=200)

def confirm_destoring(request, reservation_id, reservated_destoring_item_id):
    if request.method == "DELETE":
        reservated_destoring_item = get_object_or_404(Reservated_Destoring_Item, pk=reservated_destoring_item_id)
        stored_item = get_object_or_404(Stored_Item, pk=reservated_destoring_item.stored_item_id.stored_item_id)
        # Check if all items of this location is getting destored or only a part of them
        if stored_item.stored_item_quantity >= reservated_destoring_item.reservated_destoring_item_quantity:
            stored_item.stored_item_quantity -= reservated_destoring_item.reservated_destoring_item_quantity
            stored_item.save()
        else:
            stored_item.delete()
        reservated_destoring_item.delete()
        # Check if all items are destored
        if len(Reservated_Destoring_Item.objects.filter(reservation_id = reservation_id)) == 0:
            reservation = get_object_or_404(Reservation, pk=reservation_id)
            reservation.delete()
            data = {"destoring_end": True}
            return JsonResponse(data)
        else:
            data = {"destoring_end": False}
            return JsonResponse(data)
    return  HttpResponse("Reservation deleted", status=200)

def cancel_destoring(request, reservation_id):
    if request.method == "DELETE":
        # Get the reservation and delete it with all it's reservated items
        reservation = get_object_or_404(Reservation, pk=reservation_id)
        reservation.delete()
    return  HttpResponse("Reservation deleted", status=200)