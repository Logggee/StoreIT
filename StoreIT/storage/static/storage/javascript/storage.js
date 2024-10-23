// Function displays or hides items of the master data set which names matches the input field
function filterItems() {
    // Get the value from the input field
    let input = document.getElementById('master-data-search-field').value.toLowerCase();
    
    // Get the list of items
    let items = document.getElementById('master-data-list').getElementsByTagName('li');
    
    // Loop through all items and hide those that don't match the search query
    for (let i = 0; i < items.length; i++) {
        let item_name = items[i].innerText.toLowerCase();
        if (item_name.includes(input)) {
            items[i].classList.remove("d-none")  // Display item if it is a match
            console.log("Displaying Item: ", items[i].innerText);
        } 
        else {
            items[i].classList.add("d-none")  // Hide item if it doesn't match
            console.log("Hiding Item: ", items[i].innerText);
        }
    }
}
