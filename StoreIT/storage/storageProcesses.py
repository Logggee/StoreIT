from .models import Stored_Item, Bin, Item, Reservation, Reservated_Destoring_Item, Reservated_Storing_Item
from .forms import Store_Item_Form
from django.shortcuts import get_object_or_404

def destore_item(item_id, destore_quantity) -> list:
    ''' Destores a item after the LIFO priciple

    Args:
        item_id: primary key of a item
        destore_quantity: The quantity that the user wants to destore

    Returns:
        destore_places_and_quantitys: A list of dicts. Each dict holds the data for every destore modal that needs to be shown.
            All values need to be extracted from the db because it gets safed in the session storage so no query object is
            possible to use in this case.
    '''
    destore_places_and_quantitys = list()
    destore_complete = False
    # Get a LIFO list of all stored items of the item
    first_in_first_out = Stored_Item.get_stored_item_last_in_first_out_list(item_id)
    print(f"First in first out: {first_in_first_out}")
    # Itterate over all storage bins as long as the required amount is destored
    # This itteraton works with the FIFO principle
    for stored_item in first_in_first_out:
        # Check if the stored amount at this storage place is enough
        if stored_item.stored_item_quantity > destore_quantity:
            # Destore the amount and safe the new amount
            stored_item.stored_item_quantity -= destore_quantity
            destored_quantity_at_current_location = destore_quantity
            stored_item.save()
            destore_complete = True
            
        # If the stored amount was not enough delete the stored item and move to the next storage place
        else:
            # Calculate the delta 
            destore_quantity -= stored_item.stored_item_quantity
            destored_quantity_at_current_location = stored_item.stored_item_quantity
            # Delete the stored item because it was fully destored
            stored_item.delete()

        
        destore_places_and_quantitys.append({"destore_bin_id": stored_item.bin_id.bin_id,
                                             "destored_item_name": stored_item.item_id.item_name,
                                             "destored_item_image": stored_item.item_id.item_image.url,
                                             "destored_storage_id": stored_item.bin_id.storage_id.storage_id,
                                             "destored_storage_name": stored_item.bin_id.storage_id.storage_name,
                                             "destored_bin_number": stored_item.bin_id.bin_number,
                                             "destored_quantity": destored_quantity_at_current_location})
        if destore_complete:
            return destore_places_and_quantitys
        
    return destore_places_and_quantitys

def store_existing_item(request, store_item_form, item_id):
    # Get all same stored items
    stored_items = Stored_Item.objects.filter(item_id = item_id)
    last_in_first_out_list = Stored_Item.get_stored_item_last_in_first_out_list(item_id)
    # Check if the item already exists in the storage
    if last_in_first_out_list:
        stored_item = last_in_first_out_list[0]
        # Add the quantity to the already stored same item
        # TODO here the correct storage place needs to be calculated
        stored_item.stored_item_quantity += store_item_form.cleaned_data["item_quantity"]
        stored_item.save()
        # Create a reservation for the added quantity
        reservation = Reservation(user_id = request.user)
        reservation.save()

        reservation_item = Reservated_Storing_Item(reservation_id = reservation,
                                                   stored_item_id = stored_item,
                                                   reservated_storing_item_quantity = store_item_form.cleaned_data["item_quantity"])
        reservation_item.save()
        return stored_item, reservation.reservation_id

        
    # Item did not exist in the storage so a new Stored_Item dataset needs to be added
    # Item was only in the master date from earlyer times
    else:
        storage_bin = Bin.objects.get(pk = 10)
        item = Item.objects.get(pk = item_id)
        stored_item = Stored_Item(bin_id = storage_bin,
                                    item_id = item,
                                    stored_item_quantity = store_item_form.cleaned_data["item_quantity"])
        stored_item.save()

        reservation = Reservation(user_id = request.user)
        reservation.save()

        reservation_item = Reservated_Storing_Item(reservation_id = reservation,
                                                    stored_item_id = stored_item,
                                                    reservated_storing_item_quantity = store_item_form.cleaned_data["item_quantity"])
        reservation_item.save()

        #TODO Algo for searching for the last bin where same item was stored to add this item
        print(stored_items)
        return stored_item, reservation.reservation_id
    
def store_new_item(request, store_item_form):
    # Modal form this directly adds a new item to the db
    new_item = store_item_form.save()
    # Add a new stored item to the database
    # TODO Storage algorythm goes here
    new_stored_item = Stored_Item (bin_id = Bin.objects.get(pk=5),
                                    item_id = new_item,
                                    stored_item_quantity = store_item_form.cleaned_data["item_quantity"])
    new_stored_item.save()

    reservation = Reservation(user_id = request.user)
    reservation.save()

    reservation_item = Reservated_Storing_Item(reservation_id = reservation,
                                                   stored_item_id = new_stored_item,
                                                   reservated_storing_item_quantity = store_item_form.cleaned_data["item_quantity"])
    reservation_item.save()
    return 