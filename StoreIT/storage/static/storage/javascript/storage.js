// Function displays or hides items of the master data set which names matches the input field
function searchMasterData () {
    // Get the value from the input field and split it by spaces into an array of search terms
    let input = document.getElementById('master-data-search-field').value.toLowerCase().trim();
    let searchTerms = input.split(/\s+/); // Split by spaces, handling multiple spaces

    // Get the list of items
    let items = document.getElementById('master-data-list').getElementsByTagName('li');
    
    // Loop through all items and hide those that don't match the search query
    for (let i = 0; i < items.length; i++) {
        let item_name = items[i].innerText.toLowerCase();
        let match = true;

        // Check if every search term is present in the item name
        searchTerms.forEach(function(term) {
            if (!item_name.includes(term)) {
                match = false; // If one term is missing, this item is not a match
            }
        });

        if (match) {
            items[i].classList.remove("d-none");  // Display item if all terms match
        } 
        else {
            items[i].classList.add("d-none");  // Hide item if any term doesn't match
        }
    }
}

// User can only select one checkbox in master data search list
function onlyOneSelectable (checkbox) {
    let form = document.getElementById("add-new-item-form");
    let checkboxes = document.getElementsByName('master-data-list-checkbox'); // query all checkboxes
    // Uncheck every checkbox except the checkbox that called the function
    checkboxes.forEach((item) => { 
        if (item !== checkbox) {
            item.checked = false;
        }
    });
    // Prefill all form fields with the check items values
    if (checkbox.checked) {
        checkbox_id = checkbox.id;
        item_id = checkbox_id.split('-').pop()

        fetch(`/storage/${item_id}`)
            .then(response => response.json())
            .then(response_data => {
                document.getElementById("item-image-label").classList.add("d-none");
                document.getElementById("item-image").classList.add("d-none");
                document.getElementById("item-name").value = response_data.item_name;
                document.getElementById("item-name").setAttribute("readonly", true);
                document.getElementById("item-note").value = response_data.item_note;
                document.getElementById("item-note").setAttribute("readonly", true);
                document.getElementById("item-datasheet-label").classList.add("d-none");
                document.getElementById("item-datasheet").classList.add("d-none");
                document.getElementById("item-datasheet-selected-master-data-label").classList.remove("d-none");
                document.getElementById("item-datasheet-selected-master-data").classList.remove("d-none");
                document.getElementById("item-datasheet-selected-master-data").setAttribute("placeholder", response_data.item_datasheet);
                document.getElementById("item-purchase-place").setAttribute("placeholder",response_data.item_purchase_place);
                document.getElementById("item-purchase-place").setAttribute("readonly", true);
                document.getElementById("item-volume").value = response_data.item_volume;
                document.getElementById("item-volume").setAttribute("readonly", true);

                // Set the url to parse the primary key of the already existing item
                form.action = `/storage/store_existing_item/${response_data.item_id}`;
            })  
    }
    // If the checkbox was unchecked empty all all form fields
    else {
        document.getElementById("item-image-label").classList.remove("d-none");
        document.getElementById("item-image").classList.remove("d-none");
        document.getElementById("item-name").value = "";
        document.getElementById("item-name").removeAttribute("readonly");
        document.getElementById("item-note").value = "";
        document.getElementById("item-note").removeAttribute("readonly");
        document.getElementById("item-datasheet-label").classList.remove("d-none");
        document.getElementById("item-datasheet").classList.remove("d-none");
        document.getElementById("item-datasheet-selected-master-data-label").classList.add("d-none");
        document.getElementById("item-datasheet-selected-master-data").classList.add("d-none");
        document.getElementById("item-purchase-place").value = "";
        document.getElementById("item-purchase-place").removeAttribute("readonly");
        document.getElementById("item-volume").value = "";
        document.getElementById("item-volume").removeAttribute("readonly");
        form.action = "storage/store_new_item";
    }
}

function showOnlySearchHits (input_field) {
    // Get the value from the input field and split it by spaces into an array of search terms
    let input = input_field.value.toLowerCase().trim();
    let searchTerms = input.split(/\s+/); // Split by spaces, handling multiple spaces

    // Get all cards
    const cards = document.querySelectorAll('.card');

    cards.forEach((card) => {
        card_title = card.querySelector("h4.card-title");
        let match = true;

        if (card_title) {
            const item_name = card_title.innerText.toLowerCase();

            // Check if every search term is present in the item name
            searchTerms.forEach(function(term) {
                if (!item_name.includes(term)) {
                    match = false; // If one term is missing, this item is not a match
                }
            });

            if (match) {
                card.classList.remove("d-none");  // Display item if all terms match
            }

            else {
                card.classList.add("d-none");  // Hide item if any term doesn't match
            }
        }
    });
}

function addItemToDestoreList (item_id) {
    const destore_list = document.getElementById("destore-list");
    // Check if the list was empty till now show all buttons
    if (destore_list.childElementCount == 0) {
        document.getElementById("destore-list-empty-text").classList = "d-none";
        document.getElementById("destore-list-delete-item-button").classList.remove("d-none");
        document.getElementById("destore-list-destore-button").classList.remove("d-none");
    }

    if (document.getElementById("destore_list_item_" + item_id) != null) {
        let quantity_span = document.getElementById("destore_list_item_" + item_id);
        quantity_span.innerText = parseInt(quantity_span.innerText, 10) + 1;
    }
    else {
        const list_item = document.createElement("li");
        list_item.classList = "list-group-item d-flex align-items-center";

        const div_quantity = document.createElement("div");
        div_quantity.classList = "container d-flex align-items-center justify-content-end";
        div_quantity.innerText = "Quantity: ";

        const quantity = document.createElement("span");
        quantity.id = "destore_list_item_" + item_id;
        quantity.classList = "align-middle mx-3";
        quantity.innerText = "1";

        div_quantity.appendChild(quantity);

        const item_image = document.createElement("img");
        item_image.classList = "ms-2 destore-list-image";

        const checkbox = document.createElement("input");
        checkbox.classList = "form-check-input ms-auto";
        checkbox.type = "checkbox";
        checkbox.value = "";
        checkbox.name = "destore-list-checkbox";

        const div_item_name = document.createElement("div");
        div_item_name.classList = "container";

        // Fetch the data of the added item via a ajax call
        fetch(`/storage/${item_id}`)
            .then(response => response.json())
            .then(response_data => {
                div_item_name.innerText =  response_data.item_name;
                list_item.appendChild(div_item_name);
                item_image.src = response_data.item_image;
                item_image.alt = response_data.item_name;
                list_item.appendChild(item_image);
                list_item.appendChild(div_quantity);
                list_item.appendChild(checkbox);
                destore_list.appendChild(list_item);
            })
    }
}

function deleteItemDestoringList () {
    // TODO deleting of multiple items not working
    destore_list_checkboxes = document.getElementsByName("destore-list-checkbox");
    destore_list_checkboxes.forEach((checkbox) => {
        if (checkbox.checked) {
            // Remove the li element where the checkbox was set
            checkbox.parentNode.parentNode.removeChild(checkbox.parentNode);
        }
    });

    // Check if the list is now empty to show the empty text again and remove the delete and destore button
    const destore_list = document.getElementById("destore-list");
    if (destore_list.childElementCount == 0) {
        document.getElementById("destore-list-empty-text").classList = "";
        document.getElementById("destore-list-delete-item-button").classList.add("d-none");
        document.getElementById("destore-list-destore-button").classList.add("d-none");
    }
}

async function storage_process_confirmed (reservation_id) {
    // Confirm the storage process

    try {
        const response = await fetch(`/storage/confirm_storing/${reservation_id}`, {
            method: 'DELETE',
            headers: {
                'X-CSRFToken': csrftoken, // Parse the csfr token
            }
        });

        if (response.ok) {
            location.reload();
        } else {
            //alert('Error deleting item.');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('An error occurred while deleting the item.');
    }
}

async function storage_process_canceld (reservation_id) {
    // Cancel the storage process
    try {
        const response = await fetch(`/storage/cancel_storing/${reservation_id}`, {
            method: 'DELETE',
            headers: {
                'X-CSRFToken': csrftoken, // Parse the csfr token
            }
        });

        if (response.ok) {
            location.reload();
        } else {
            //alert('Error deleting item.');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('An error occurred while deleting the item.');
    }
}

async function destoring_process_confirmed (reservation_id, reservated_destoring_item)  {

    // Confirm the destoring process
    try {
        const response = await fetch(`/storage/confirm_destoring/${reservation_id}/${reservated_destoring_item}`, {
            method: 'DELETE',
            headers: {
                'X-CSRFToken': csrftoken, // Parse the csfr token
            }
        });

        const response_data = await response.json();

        if (response_data.destoring_end == true) {
            location.reload();
        }
        
    } catch (error) {
        console.error('Error:', error);
        alert('An error occurred while deleting the item.');
    }
}

async function destoring_process_canceld (reservation_id) {
    // Cancel the destoring process
    console.log("Test");

    try {
        const response = await fetch(`/storage/cancel_destoring/${reservation_id}`, {
            method: 'DELETE',
            headers: {
                'X-CSRFToken': csrftoken, // Parse the csfr token
            }
        });

        if (response.ok) {
            location.reload();
        } else {
            //alert('Error deleting item.');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('An error occurred while deleting the item.');
    }
}

function add_inputs_manual_quantity (checkbox, storage_id, bin_id, bin_number) {
    const div = document.getElementById("bin-manual-quantity-" + storage_id);

    if (checkbox.checked) {
        if (div.childNodes.length === 0) {
            const grayLine = document.createElement("div");
            grayLine.classList = "container-fluid my-3";
            grayLine.id = "gray-line-manual-storage"
            grayLine.style.borderTop = "solid 1px gray";
            div.appendChild(grayLine);
        }

        const input_div = document.createElement("div");
        input_div.classList = "mb-3";
        input_div.id = "manual-quantity-div-" + bin_id + "-" + bin_number;

        const row = document.createElement("row");
        row.classList = "row";
        row.id = "manual-quantity-input-row-" + bin_id;

        const col_1 = document.createElement("div");
        col_1.classList = "col-3";

        const col_2 = document.createElement("div");
        col_2.classList = "col-9";

        const label = document.createElement("label");
        label.classList = "form-label";
        label.for = "manual-quantity-input-" + bin_id;
        label.innerText = "Bin number " + bin_number;

        const input = document.createElement("input");
        input.type = "number";
        input.classList = "form-control";
        input.id = "manual-quantity-input-" + bin_id;
        input.name = "manual-quantity-input";
        input.placeholder = "Enter quantity for bin " + bin_number;
        input.min = 1;

        col_1.appendChild(label);
        col_2.appendChild(input);
        row.appendChild(col_1);
        row.appendChild(col_2);
        input_div.appendChild(row);
        div.appendChild(input_div);
    }
    else {
        document.getElementById("manual-quantity-input-row-" + bin_id).remove();

        if (div.children.length === 1) {
            document.getElementById("gray-line-manual-storage").remove();
        }
    }
}
/* User wants to select a storage location manually

*/
async function stored_item_manually (reservation_id) {
    let json_data = {"reservation_id": reservation_id, "bins_and_quantitys": []};
    let all_manual_quantity_inputs = document.getElementsByName("manual-quantity-input");

    all_manual_quantity_inputs.forEach((manual_quantity_input) => {
        split_string = manual_quantity_input.id.split("-");
        bin_id = split_string[split_string.length - 1];
        quantity = manual_quantity_input.value;
        json_data["bins_and_quantitys"].push({ bin_id: bin_id, quantity: quantity });
    });

    try {
        const response = await fetch('/storage/manual_storage', {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken,
            },
            body: JSON.stringify(json_data)
        });
    
        if (response.ok) {
            window.location.href = "/storage/"
        } 
        else {
            alert('Error accured while trying to store the items manualy!');
        }
    }
    catch (error) {
        console.error('Error:', error);
        alert('An error occurred while deleting the item.');
    }
}