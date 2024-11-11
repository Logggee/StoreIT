from .models import Stored_Item, Bin

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
    destore_place_and_quantity = dict()
    destore_places_and_quantitys = list()
    # Get a FIFO list of all stored items of the item
    first_in_first_out = Stored_Item.get_stored_item_last_in_first_out_list(item_id)
    # Itterate over all storage bins as long as the required amount is destored
    # This itteraton works with the FIFO principle
    for stored_item in first_in_first_out:
        # Check if the stored amount at this storage place is enough
        if stored_item.stored_item_quantity > destore_quantity:
            # Safe the destore place and destored quantity to return it
            destore_place_and_quantity["destore_bin_id"] = stored_item.bin_id.bin_id
            destore_place_and_quantity["destored_item_name"] = stored_item.item_id.item_name
            destore_place_and_quantity["destored_item_image"] = stored_item.item_id.item_image
            destore_place_and_quantity["destored_storage_id"] = stored_item.bin_id.storage_id.storage_id
            destore_place_and_quantity["destored_storage_name"] = stored_item.bin_id.storage_id.storage_name
            destore_place_and_quantity["destored_bin_number"] = stored_item.bin_id.bin_number
            destore_place_and_quantity["destored_quantity"] = destore_quantity
            destore_places_and_quantitys.append((destore_place_and_quantity))
            # Destore the amount and safe the new amount
            stored_item.stored_item_quantity -= destore_quantity
            stored_item.save()
            return destore_places_and_quantitys
        # If the stored amount was not enough delete the stored item and move to the next storage place
        else:
            # Calculate the delta 
            destore_quantity -= stored_item.stored_item_quantity
            destore_place_and_quantity["destore_bin_id"] = stored_item.bin_id.bin_id
            destore_place_and_quantity["destored_item_name"] = stored_item.item_id.item_name
            destore_place_and_quantity["destored_item_image"] = stored_item.item_id.item_image
            destore_place_and_quantity["destored_storage_id"] = stored_item.bin_id.storage_id.storage_id
            destore_place_and_quantity["destored_storage_name"] = stored_item.bin_id.storage_id.storage_name
            destore_place_and_quantity["destored_bin_number"] = stored_item.bin_id.bin_number
            destore_place_and_quantity["destored_quantity"] = destore_quantity
            # Safe the destore place to return it
            destore_places_and_quantitys.append((destore_place_and_quantity))
            # Delete the stored item because it was fully destored
            stored_item.delete()
    return destore_places_and_quantitys