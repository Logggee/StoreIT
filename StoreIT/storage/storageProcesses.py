from .models import Stored_Item

def destore_item(item_id, destore_quantity):
    first_in_first_out = Stored_Item.get_stored_item_last_in_first_out_list(item_id)
    for stored_item in first_in_first_out:
        if stored_item.stored_item_quantity > destore_quantity:
            stored_item.stored_item_quantity -= destore_quantity
            stored_item.save()
            return
        else:
            destore_quantity -= stored_item.stored_item_quantity
            stored_item.delete()
    return