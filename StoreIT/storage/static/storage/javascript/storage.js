// Function displays or hides items of the master data set which names matches the input field
function filterItems() {
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
            console.log("Displaying Item: ", items[i].innerText);
        } 
        else {
            items[i].classList.add("d-none");  // Hide item if any term doesn't match
            console.log("Hiding Item: ", items[i].innerText);
        }
    }
}

// User can only select one checkbox in master data search list
function onlyOneSelectable(checkbox) {
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
                document.getElementById("item-image-file-label").classList.add("d-none")
                document.getElementById("item-image-file").classList.add("d-none")
                document.getElementById("item-name").value = response_data.item_name;
                document.getElementById("item-name").setAttribute("readonly", true);
                document.getElementById("item-node").value = response_data.item_node;
                document.getElementById("item-node").setAttribute("readonly", true);
                document.getElementById("item-datasheet").value = response_data.item_datasheet;
                document.getElementById("item-datasheet").setAttribute("readonly", true);
                document.getElementById("item-purshase-place").value = response_data.item_purshase_place;
                document.getElementById("item-purshase-place").setAttribute("readonly", true);
            })
    }
    // If the checkbox was unchecked empty all all form fields
    else {
        document.getElementById("item-image-file-label").classList.remove("d-none")
        document.getElementById("item-image-file").classList.remove("d-none")
        document.getElementById("item-name").value = "";
        document.getElementById("item-name").removeAttribute("readonly");
        document.getElementById("item-node").value = "";
        document.getElementById("item-node").removeAttribute("readonly");
        document.getElementById("item-datasheet").value = "";
        document.getElementById("item-datasheet").removeAttribute("readonly");
        document.getElementById("item-purshase-place").value = "";
        document.getElementById("item-purshase-place").removeAttribute("readonly");
    }
}