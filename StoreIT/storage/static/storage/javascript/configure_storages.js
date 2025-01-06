//config.js

function generateCollumnInputFields(input) {
    // Prevent manual input of 0
    if (input.value == 0) {
        input.value = 1;
    }
    // Get the number of rows from the user input
    const numberOfRows = parseInt(input.value);
    // Get and safe the existing bins per row input fields
    const container_row = document.getElementById("container-columns");
    rows_inputs = Array.from(container_row.children);
    // Clear all bins per row input fields
    container_row.innerHTML = "";
    // Create a new number of bins per row input field for every row
    for (let i = 0; i < numberOfRows; i++) {
        const colDiv = document.createElement("div");
        colDiv.className = "container col-3";

        const label = document.createElement("label");
        label.className = "col-form-label";
        label.innerText = "Number of bins of row " + (i + 1) + ":";
        
        const inputField = document.createElement("input");
        inputField.type = "number";
        inputField.className = "form-control number-of-bins-row";
        inputField.placeholder = "n bins";
        inputField.min = "1";
        inputField.name = "number-of-bins-row-" + (i + 1);
        inputField.required = true;
        inputField.id = (i + 1);
        inputField.max = 20;
        inputField.min = 1;
        inputField.oninput = function() {
            generateStorageLayout(this, i+1);
        };
        // For every input field that already existed prefill the the old value
        if (i < rows_inputs.length && rows_inputs.length != 0) {
            old_input_field = rows_inputs[i].querySelector("input");
            inputField.value = old_input_field.value;
        }

        const validationField = document.createElement("div");
        validationField.classList = "invalid-feedback";
        validationField.id = "invalid-feedback-number-of-bins-row-" + (i + 1);
        
        colDiv.appendChild(label);
        colDiv.appendChild(inputField);
        colDiv.appendChild(validationField);
        
        container_row.appendChild(colDiv);
    }

    // If the number of rows is decremented the last row/rows of the layout needs to be deleted
    const container_storage_layout = document.getElementById("storage-layout-container");
    // Calculate how many rows need to be deleted to match the new rows input
    const delete_n_rows = container_storage_layout.children.length - numberOfRows;
    for (let i = 0; i < delete_n_rows; i++) {
        container_storage_layout.removeChild(container_storage_layout.lastChild);
    }

    // Check how much diffrent bin sizes exists after the changes
    let diffret_bin_sizes = [];
    const rows = container_row.children;
    for(let i = 0; i < rows.length; i++) {
        if (!diffret_bin_sizes.includes(rows[i].querySelector("input").value)) {
            diffret_bin_sizes.push(rows[i].querySelector("input").value);
        }
    }
    // Remove a bin size input field if needed after the rows number has changed
    const container_bin_sizes = document.getElementById("container-bin-sizes-row");
    // Calculate how many bin volume input fields need to be removed 
    delete_n_elements = container_bin_sizes.children.length - diffret_bin_sizes.length;
    for (let i = 0; i < delete_n_elements; i++) {
        container_bin_sizes.removeChild(container_bin_sizes.lastChild);
    }
}


function generateStorageLayout(input, row_number) {
    // Prevent manual input of 0
    if (input.value == 0) {
        input.value = 1;
    }
    // Add the heading of storage layout and all of the gray lines and safe config button
    storage_layout_heading_container = document.getElementById("storage-layout-heading-container");
    // Check if the heading, gray seperating lines and safe button already exists and if not create them
    if (!document.getElementById("storage-layout-heading")){
        // Create the heading for the storage layout
        const storage_layout_heading = document.createElement("p");
        storage_layout_heading.id = "storage-layout-heading";
        storage_layout_heading.innerHTML = "Configured layout of the storage";
        storage_layout_heading_container.insertBefore(storage_layout_heading, storage_layout_heading_container.firstChild);
        // Add the gray lines for seperating the diffrent rows
        const storage_layout_form = document.getElementById("storage-layout-form");
        storage_layout_form.insertBefore(createGrayLine(), document.getElementById("row-storage-layout"));
        storage_layout_form.insertBefore(createGrayLine(), document.getElementById("container-bin-sizes-heading"));
        storage_layout_form.insertBefore(createGrayLine(), document.getElementById("row-safe-config"));
        // Add the safe config button
        const container_safe_config_button = document.getElementById("container-safe-config-button");
        let safe_config_button = document.createElement("button");
        safe_config_button.type = "button";
        safe_config_button.classList = "btn btn-success mt-3 d-flex align-items-center";
        safe_config_button.id = "button-safe-config";
        // Append the button icon and make it visible
        const safe_config_button_image = document.getElementById("safe-config-button-image");
        safe_config_button_image.style = "";
        safe_config_button.onclick = () => {
            // Validate the form
            if (!validate_add_new_storage_form()) {
                // If form was valid submit it
                document.getElementById("storage-layout-form").submit();
            }
        };
        // Append the button before adding the text of the button
        safe_config_button.appendChild(safe_config_button_image);
        container_safe_config_button.appendChild(safe_config_button);
        // Get the button again to add the text so the icon is left of the text
        safe_config_button = document.getElementById("button-safe-config");
        const textNode = document.createTextNode("Save configuration");
        safe_config_button.appendChild(textNode);
    }
    // Get the new value of the changed bins input
    const number_of_bins = parseInt(input.value);
    const container_storage_layout = document.getElementById("storage-layout-container");
    // Create a new row for the storage layout with the new number of bins in the row
    const div_row = document.createElement("div");
    div_row.className = "row mb-2 align-items-center";
    div_row.id = "storage-layout-row-" + row_number;
    
    const span = document.createElement("span");
    span.classList = "col-auto";
    span.innerText = "Row " + row_number;
    span.style = "min-width: 80px"; // Adopt for double digid row numbers
    div_row.appendChild(span);

    const div_col = document.createElement("div");
    div_col.className = "col d-flex justify-content-between mx-4";
    div_col.id = "storage-layout-col-" + row_number;

    for (let i = 0; i < number_of_bins; i++) {
        const input = document.createElement("input");
        input.type = "radio";
        input.className = "btn-check";
        input.name = "btnradio";
        input.id = "btnradio" + row_number + "-" + i;
        input.autocomplete = "off";
        div_col.appendChild(input);

        const label = document.createElement("label");
        label.classList = "btn btn-outline-primary w-100 me-1";
        label.for = "btnradio" + row_number + "-" + i;
        label.innerText = i + 1
        div_col.appendChild(label);
    }

    div_row.appendChild(div_col);

    // Get all existing rows in a array to avoid getting a refernce of the childs
    const rows = Array.from(container_storage_layout.children);
    // Append the row as the first element in the array
    rows.unshift(div_row);
    // All childs are saved in the array so all childs can be deleted
    container_storage_layout.innerHTML = "";
    let smaller_row, bigger_row;

    // Move the new row as long to the right until it is at the rigth position
    for (let i = 0; i < rows.length - 1; i++) {
        if (parseInt(rows[i].id.match(/(\d+)/)) > parseInt(rows[i + 1].id.match(/(\d+)/))) {
            smaller_row = rows[i + 1];
            bigger_row = rows[i];
            rows[i] = smaller_row;
            rows[i + 1] = bigger_row;
        }
        // If the row number already existed delete the old row
        else if (parseInt(rows[i].id.match(/(\d+)/)) == parseInt(rows[i + 1].id.match(/(\d+)/))) {
            rows.splice(i + 1, 1);
        }
    }
    let diffret_bin_sizes = [];
    // After soting all rows into the right order append all rows the the container
    rows.forEach((row) => {
        let number_of_bins = row.querySelectorAll("input");
        if (!diffret_bin_sizes.includes(number_of_bins.length)) {
            diffret_bin_sizes.push(number_of_bins.length);
        }
        container_storage_layout.appendChild(row);
    });

    // Add the heading for the diffrent bin sizes
    const container_bin_sizes_heading = document.getElementById("container-bin-sizes-heading");
    if (!document.getElementById("bin-sizes-heading")){
        const bin_sizes_heading = document.createElement("p");
        bin_sizes_heading.id = "bin-sizes-heading";
        bin_sizes_heading.innerText = "Enter the volumes of the diffrent bin sizes";
        container_bin_sizes_heading.insertBefore(bin_sizes_heading, container_bin_sizes_heading.firstChild);
    }

    // Build the input fields for the bin sizes
    const container_bin_sizes_row = document.getElementById("container-bin-sizes-row");
    //const bin_sizes = Array.from(container_bin_sizes.children);
    container_bin_sizes_row.innerHTML = "";
    const sizes = ["S", "M", "L", "XL", "XXL", "XXXL", "XXXXL", "XXXXXL"];

    for (let i = 0; i < diffret_bin_sizes.length; i++) {
        const div_bin_size_col = document.createElement("div");
        div_bin_size_col.classList = "container col-3";

        div_bin_size = document.createElement("div");
        div_bin_size.classList = "mb-3 text-start";

        label_bin_size = document.createElement("label");
        label_bin_size.for = "bin-size-" + sizes[i];
        label_bin_size.classList = "col-form-label";
        label_bin_size.innerText = "Volume of " + sizes[i] + " bin";
        div_bin_size.appendChild(label_bin_size);

        input_bin_size = document.createElement("input");
        input_bin_size.type = "number";
        input_bin_size.classList = "form-control volume";
        input_bin_size.id = sizes[i];
        input_bin_size.name = "bin-size-" + sizes[i];
        input_bin_size.placeholder = "Volume in ccm";
        input_bin_size.min = "1";
        input_bin_size.max = "1000000";
        div_bin_size.appendChild(input_bin_size);

        const validationField = document.createElement("div");
        validationField.classList = "invalid-feedback";
        validationField.id = "invalid-feedback-bin-size-" + sizes[i];
        div_bin_size.appendChild(validationField);

        div_bin_size_col.appendChild(div_bin_size);
        container_bin_sizes_row.appendChild(div_bin_size_col);
    }
}
// Helper function for creating a gray seperator line element
function createGrayLine() {
    const grayLine = document.createElement("div");
    grayLine.classList = "container-fluid my-3";
    grayLine.style.borderTop = "solid 1px gray";
    return grayLine;
}

function validate_add_new_storage_form() {
    let form_invalid = false;
    // Validate storage name field
    const storage_name = document.getElementById("storage-name");
    storage_name.classList.remove("is-invalid");
    const invalid_feedback_storage_name = document.getElementById("invalid-feedback-storage-name");
    if (storage_name.value.length <= 0) {
        storage_name.classList += " " + "is-invalid";
        invalid_feedback_storage_name.innerText = "You need to name your storage";
        form_invalid = true;
    }
    else if (storage_name.value.length > 30) {
        storage_name.classList += " " + "is-invalid";
        invalid_feedback_storage_name.innerText = "Your storage name cant be longer then 30 characters";
        form_invalid = true;
    }

    // Validate storage rows
    const storage_rows = document.getElementById("storage-rows");
    storage_rows.classList.remove("is-invalid");
    const invalid_feedback_storage_rows = document.getElementById("invalid-feedback-storage-rows");
    if (storage_rows.value <= 0) {
        storage_rows.classList += " " + "is-invalid";
        invalid_feedback_storage_rows.innerText = "Number of rows needs to be bigger then 0";
        form_invalid = true;
    }
    else if (storage_rows.value > 30) {
        storage_rows.classList += " " + "is-invalid";
        invalid_feedback_storage_rows.innerText = "Your storage cant have more then 30 rows";
        form_invalid = true;
    }

    // Validation of bins per row
    const all_bins_per_row = document.getElementsByClassName("form-control number-of-bins-row");
    for (let i=0; i<all_bins_per_row.length; i++)
    {
        all_bins_per_row[i].classList.remove("is-invalid");
        const invalid_feedback_number_of_bins_row = document.getElementById("invalid-feedback-number-of-bins-row-" + all_bins_per_row[i].id);
        if (all_bins_per_row[i].value <= 0) {
            all_bins_per_row[i].classList += " " + "is-invalid";
            invalid_feedback_number_of_bins_row.innerText = "Number of bins needs to be bigger then 0";
            form_invalid = true;
        }
        else if (all_bins_per_row[i].value > 20) {
            all_bins_per_row[i].classList += " " + "is-invalid";
            invalid_feedback_number_of_bins_row.innerText = "Your row cant have more then 20 bins";
            form_invalid = true;
        }
    }

    // Validation of bin volumes
    const all_bin_sizes = document.getElementsByClassName("form-control volume");
    let lastVolume = null;
    let fieldInvlalid = false;
    for (let i=0; i<all_bin_sizes.length; i++)
    {
        // Remove old validation Error Message
        all_bin_sizes[i].classList.remove("is-invalid");
        volume = parseFloat(all_bin_sizes[i].value);
        const invalid_feedback_bin_size = document.getElementById("invalid-feedback-bin-size-" + all_bin_sizes[i].id);
        if (all_bin_sizes[i].value <= 0) {
            all_bin_sizes[i].classList += " " + "is-invalid";
            invalid_feedback_bin_size.innerText = "This field cant be empty";
            fieldInvlalid = true;
            form_invalid = true;
        }
        else if (volume <= 0) {
            all_bin_sizes[i].classList += " " + "is-invalid";
            invalid_feedback_bin_size.innerText = "Volume must be bigger then 0";
            fieldInvlalid = true;
            form_invalid = true;
        }
        else if (volume > 1000000) {
            all_bin_sizes[i].classList += " " + "is-invalid";
            invalid_feedback_bin_size.innerText = "Volume cant be bigger then 10 dm^3";
            fieldInvlalid = true;
            form_invalid = true;
        }
        
        if (lastVolume == null) {
            lastVolume = volume
        }
        else {
            if (volume <= lastVolume &&  !fieldInvlalid) {
                all_bin_sizes[i].classList += " " + "is-invalid";
                invalid_feedback_bin_size.innerText = "Volume must be bigger than the volume of the next smaller bin";
                fieldInvlalid = true;
                form_invalid = true;
            }
            else {
                lastVolume = volume;
            }
        } 
    }

    return form_invalid;
}

// Function for fetch call to get all items that are stored in a specific bin
function get_all_items_of_bin(bin_id) {
    // Make the table visible
    table_container = document.getElementById("container-table");
    table_container.classList = "container";
    // Fetch all items that are stored in the selected bin
    fetch(`/config/${bin_id}`)
        .then(response => response.json())
        .then(response_data => {
            // Clear the previos table content
            const table = document.getElementById("table");
            table.innerHTML = "";

            // Build a table row for every item in this bin
            for (let i = 0; i < response_data.length; i++) {
                // Extract one item of the dict, the item is also a dict
                stored_item = response_data[i];
    
                const table_row = document.createElement("tr");
                // First collumn is a header collumn
                const table_col_header = document.createElement("th");
                table_col_header.scope = "row";
                table_col_header.classList = "align-middle ps-3";
                table_col_header.innerText = stored_item["item_store_date_in_this_bin"];
                // Append the header col to the row
                table_row.appendChild(table_col_header);
                // Build all other collumns
                for (let j = 1; j < Object.keys(stored_item).length; j++) {
                    const table_col = document.createElement("td");
                    table_row.classList = "align-middle";
                    switch(j) {
                        case 1:
                            const item_image = document.createElement("img");
                            item_image.src = stored_item["item_image"];
                            item_image.style = "height: 50px; border-radius: 0.5rem";
                            table_col.append(item_image);
                            break;

                        case 2:
                            table_col.innerText = stored_item["item_name"];
                            break;

                        case 3:
                            table_col.innerText = stored_item["item_quantity_in_this_bin"];
                            break;
                    }
                    // Append the col to the row
                    table_row.appendChild(table_col);
                }
                // Append the whole row to the table
                table.append(table_row);
            }
        })
}

// Function is called when switching tabs
function tabSelected(storage_id) {
    table_container = document.getElementById("container-table");
    // Query the group of radio buttons of the tab storage layout
    let radio_group = document.querySelectorAll(`input[name="btnradio-${storage_id}"]`);
    // Check if a radio is set from this group
    for (let radio of radio_group) {
        // If a radio is check show the table and reload the table content
        if (radio.checked) {
            // Trigger the oncklick function to show all items in the table again
            radio.onclick()
            return;
        }
    }
    // If no radio is selected hide the table
    table_container.classList = "container d-none";
}