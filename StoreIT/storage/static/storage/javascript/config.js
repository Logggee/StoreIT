function generateCollumnInputFields(input) {
    // Prevent manual input of 0
    if (input.value == 0) {
        input.value = 1;
    }
    const numberOfRows = parseInt(input.value);  // Liest den Wert aus dem Inputfeld und konvertiert ihn in eine Zahl
    const container_row = document.getElementById("container-columns"); // Holt den Ziel-Container
    rows_inputs = Array.from(container_row.children);
    container_row.innerHTML = "";  // Leert den Container, um alte Eingabefelder zu entfernen
    
    for (let i = 0; i < numberOfRows; i++) {
        // Erzeugt ein div-Element für jede Reihe
        const colDiv = document.createElement("div");
        colDiv.className = "container col-3";

        // Erzeugt das label-Element
        const label = document.createElement("label");
        label.className = "col-form-label";
        label.innerText = `Number of bins of row ${i + 1}:`;
        
        // Erzeugt das input-Element
        const inputField = document.createElement("input");
        inputField.type = "number";
        inputField.className = "form-control";
        inputField.placeholder = "n bins";
        inputField.min = "1";
        inputField.oninput = function(){generStorageLayout(this, i+1)};
        if (i < rows_inputs.length && rows_inputs.length != 0) {
            old_input_field = rows_inputs[i].querySelector("input");
            inputField.value = old_input_field.value;
        }
        
        // Füge die Elemente zum colDiv hinzu
        colDiv.appendChild(label);
        colDiv.appendChild(inputField);
        
        // Füge colDiv dem Haupt-Container hinzu
        container_row.appendChild(colDiv);
    }

    // If the number of rows is decremented the last row/rows needs to be deleted
    const container_storage_layout = document.getElementById("storage-layout-container");
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

    const container_bin_sizes = document.getElementById("container-bin-sizes-row");
    delete_n_elements = container_bin_sizes.children.length - diffret_bin_sizes.length;
    for (let i = 0; i < delete_n_elements; i++) {
        container_bin_sizes.removeChild(container_bin_sizes.lastChild);
    }
}


function generStorageLayout(input, row_number) {
    // Prevent manual input of 0
    if (input.value == 0) {
        input.value = 1;
    }
    // Add the heading of storage layout and all of the gray lines
    storage_layout_heading_container = document.getElementById("storage-layout-heading-container");
    // Check if the heading already exists and if not create one
    if (!document.getElementById("storage-layout-heading")){
        const storage_layout_heading = document.createElement("p");
        storage_layout_heading.id = "storage-layout-heading";
        storage_layout_heading.innerHTML = "Configured layout of the storage";
        storage_layout_heading_container.insertBefore(storage_layout_heading, storage_layout_heading_container.firstChild);
        // Add the gray lines for seperating the diffrent rows
        const add_storga_tab = document.getElementById("add-tab");
        add_storga_tab.insertBefore(createGrayLine(), document.getElementById("row-storage-layout"));
        add_storga_tab.insertBefore(createGrayLine(), document.getElementById("container-bin-sizes-heading"));
        add_storga_tab.insertBefore(createGrayLine(), document.getElementById("row-safe-config"));
    }

    const number_of_bins = parseInt(input.value);
    const container_storage_layout = document.getElementById("storage-layout-container");

    const div_row = document.createElement("div");
    div_row.className = "row mb-2 align-items-center";
    div_row.id = "storage-layout-row-" + row_number;
    
    const span = document.createElement("span");
    span.classList = "col-auto";
    span.innerText = "Row " + row_number;
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
    // append the row as the first element in the array
    rows.unshift(div_row);
    // All childs are saved in the array so all childs can be deleted
    container_storage_layout.innerHTML = "";
    let smaller_row, bigger_row;

    // Move the new row as long to the right until it is at the rigth position
    for (let i = 0; i < rows.length - 1; i++) {
        if (parseInt(rows[i].id.slice(-1)) > parseInt(rows[i + 1].id.slice(-1))) {
            smaller_row = rows[i + 1];
            bigger_row = rows[i];
            rows[i] = smaller_row;
            rows[i + 1] = bigger_row;
        }
        // If the row number already existed delete the old row
        else if (parseInt(rows[i].id.slice(-1)) == parseInt(rows[i + 1].id.slice(-1))) {
            rows.splice(i + 1, 1);
        }
    }
    let diffret_bin_sizes = [];
    // Append all rows the the container
    rows.forEach((row) => {
        let number_of_bins = row.querySelectorAll("input");
        if (!diffret_bin_sizes.includes(number_of_bins.length)) {
            diffret_bin_sizes.push(number_of_bins.length);
        }
        container_storage_layout.appendChild(row);
    });

    // Add the heading
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
        input_bin_size.classList = "form-control";
        input_bin_size.id = "bin-size-" + sizes[i];
        input_bin_size.placeholder = "Volume in ccm";
        input_bin_size.min = "1";
        div_bin_size.appendChild(input_bin_size);

        div_bin_size_col.appendChild(div_bin_size);
        container_bin_sizes_row.appendChild(div_bin_size_col);
    }
}
// Helper function for creating a gray line element
function createGrayLine() {
    const grayLine = document.createElement("div");
    grayLine.classList = "container-fluid my-3";
    grayLine.style.borderTop = "solid 1px gray";
    return grayLine;
}