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
                document.getElementById("item-node").value = response_data.item_node;
                document.getElementById("item-node").setAttribute("readonly", true);
                document.getElementById("item-datasheet").value = response_data.item_datasheet;
                document.getElementById("item-datasheet").setAttribute("readonly", true);
                document.getElementById("item-purchase-place").value = response_data.item_purchase_place;
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
        document.getElementById("item-node").value = "";
        document.getElementById("item-node").removeAttribute("readonly");
        document.getElementById("item-datasheet").value = "";
        document.getElementById("item-datasheet").removeAttribute("readonly");
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

function addItemToDestoreList(item_id) {
    const destore_list = document.getElementById("destore-list");
    if (destore_list.childElementCount == 0) {
        document.getElementById("destore-list-empty-text").classList = "d-none";
        document.getElementById("destore-list-delete-item-button").classList.remove("d-none");
        document.getElementById("destore-list-destore-button").classList.remove("d-none");
    }
    const list_item = document.createElement("li");
    list_item.classList = "list-group-item d-flex align-items-center";

    const item_image = document.createElement("img");
    item_image.classList = "destore-list-image ms-2";

    const checkbox = document.createElement("input");
    checkbox.classList = "form-check-input ms-auto";
    checkbox.type = "checkbox";
    checkbox.value = "";
    checkbox.name = "destore-list-checkbox";

    // Fetch the data of the added item via a ajax call
    fetch(`/storage/${item_id}`)
        .then(response => response.json())
        .then(response_data => {
            list_item.innerText = response_data.item_name;
            item_image.src = response_data.item_image;
            item_image.alt = response_data.item_name;
            list_item.appendChild(item_image);
            list_item.appendChild(checkbox);
            destore_list.appendChild(list_item);
        })
}

function deleteItemDestoringList() {
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