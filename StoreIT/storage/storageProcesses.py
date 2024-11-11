from .models import Stored_Item

def destore_item(item_id, destore_quantity) -> list:
    ''' Destores a item after the FIFO priciple

    Args:
        item_id: primary key of a item
        destore_quantity: The quantity that the user wants to destore

    Returns:
        destore_places_and_quantitys: A list with tuples where each holds the stored item which was destored and the quantity that was destored of this stored item
    '''
    destore_places_and_quantitys = list()
    # Get a FIFO list of all stored items of the item
    first_in_first_out = Stored_Item.get_stored_item_last_in_first_out_list(item_id)
    # Itterate over all storage bins as long as the required amount is destored
    # This itteraton works with the FIFO principle
    for stored_item in first_in_first_out:
        # Check if the stored amount at this storage place is enough
        if stored_item.stored_item_quantity > destore_quantity:
            # Safe the destore place and destored quantity to return it
            destore_places_and_quantitys.append((stored_item, destore_quantity))
            # Destore the amount and safe the new amount
            stored_item.stored_item_quantity -= destore_quantity
            stored_item.save()
            return destore_places_and_quantitys
        # If the stored amount was not enough delete the stored item and move to the next storage place
        else:
            # Calculate the delta 
            destore_quantity -= stored_item.stored_item_quantity
            # Safe the destore place to return it
            destore_places_and_quantitys.append((stored_item, destore_quantity))
            # Delete the stored item because it was fully destored
            stored_item.delete()
    return destore_places_and_quantitys