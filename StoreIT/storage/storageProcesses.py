from .models import Stored_Item, Bin, Item
from .forms import Store_Item_Form

def destore_item(item_id, destore_quantity) -> list:
    ''' Destores a item after the FIFO priciple

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
    # Get a FIFO list of all stored items of the item
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

def store_existing_item(store_item_form, item_id):
    # Get all same stored items
    stored_items = Stored_Item.objects.filter(item_id = item_id)
    last_in_first_out_list = Stored_Item.get_stored_item_last_in_first_out_list(item_id)
    # Check if the item already exists in the storage
    if last_in_first_out_list:
        # TODO here the correct storage place needs to be calculated
        stored_item = last_in_first_out_list[0]
        stored_item.stored_item_quantity += store_item_form.cleaned_data["item_quantity"]
        stored_item.save()
    # Item did not exist in the storage so a new Stored_Item dataset needs to be added
    # Item was only in the master date from earlyer times
    else:
        storage_bin = Bin.objects.get(pk = 1)
        item = Item.objects.get(pk = item_id)
        stored_item = Stored_Item(bin_id = storage_bin,
                                    item_id = item,
                                    stored_item_quantity = store_item_form.cleaned_data["item_quantity"])
        stored_item.save()

    #TODO Algo for searching for the last bin where same item was stored to add this item
    print(stored_items)
    return stored_item