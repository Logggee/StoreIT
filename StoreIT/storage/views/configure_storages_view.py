# configure_storages_view.py

import re
from django.shortcuts import  render, redirect
from django.http import JsonResponse
from storage.models import Stored_Item, Bin, Storage
from storage.forms import Storage_Layout_Form
from django.contrib.auth.decorators import login_required

def config(request):
    ''' /config
    Config page

    Args:
        request: HTTP request object

    Returns:
        Renders the template config.html
    '''
    # Post request
    if request.method == "POST" and request.user.is_authenticated: 
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
                if not int(field_value) in diffrent_number_of_bin_per_row:
                    diffrent_number_of_bin_per_row.append(int(field_value))
            # Regex only matches if the string is 'bin-size-' with Capital letters after the last '-'
            elif re.match(r'bin-size-([A-Z]*)$', input_field):
                match = re.match(r'bin-size-([A-Z]*)$', input_field)
                # TODO this if is probably useless because bin sizes shoud be diffrent for each field
                # so there is no need to check if it already exist in the list because a bin size shoud always differ
                # from all other bin sizes
                if not float(field_value) in diffrent_bin_volumes:
                    diffrent_bin_volumes.append(float(field_value))
        # Sort least amount of bins per row to most numbers of bins per row
        diffrent_number_of_bin_per_row.sort()
        print(f"Diffrent number of bins per row: {diffrent_number_of_bin_per_row}")
        # Sort biggest volume to smallest volume
        diffrent_bin_volumes.sort(reverse=True)
        print(f"Diffrent bin volumes: {diffrent_bin_volumes}")
        # Build a dict where the smallest number of bins matches with the biggest volume and so on for all cobinations
        # Number of bins per row is the key and the coresponding volume is the value
        bin_volumes = dict(zip(diffrent_number_of_bin_per_row, diffrent_bin_volumes))
        print(f"Bin volumes: {bin_volumes}")
        # Build the dataset for all the bins of the new storage
        bin_number = 0
        for input_field, field_value in form_data.items():
             print(f"Input field: {input_field}")
             print(f"Field value: {field_value}")
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
                                  bin_volume = bin_volumes[float(field_value)],
                                  bin_volume_unused = 100)
                    new_bin.save()

        return redirect("storage:config")
    
    # Get request
    elif request.method == "GET":
        # Get all storages and bins
        # TODO check if list es the better datatype here because the key is maybe not relevant
        storages_and_bins = dict()
        for storage in  Storage.objects.all():
            storages_and_bins[storage] = storage.all_bins_sorted_in_rows()
        print(f"Storage and all bins: {storages_and_bins}")
        content = {"storage_layout_form": Storage_Layout_Form(),
                   "storages_and_bins": storages_and_bins,
                   "current_user": request.user}
        
        return render(request, "storage/configure_storages.html", content)
    
@login_required     
def all_items_stored_in_bin(request, bin_id):
    ''' /config/<int.bin_id>
    This endpoint gets all items that are stored in a specific bin.

    Args:
        request: HTTP request object
        bin_id: The id of the bin where the user wants to see all items stored in it

    Returns:
        Returns a JSON Object with all items that are stored in that bin
    '''
    # Get all items of the bin 
    all_items_in_bin = Stored_Item.objects.filter(bin_id = bin_id)
    data = list()
    for stored_item in all_items_in_bin:
        data.append({"item_store_date_in_this_bin" : stored_item.stored_item_storedate.strftime("%d.%m.%Y, %H:%M:%S"),
                     "item_image": stored_item.item_id.item_image.url,
                     "item_name": stored_item.item_id.item_name,
                     "item_quantity_in_this_bin": stored_item.stored_item_quantity
        })
    print(f"All items in bin {data}")
    return JsonResponse(data, safe=False)