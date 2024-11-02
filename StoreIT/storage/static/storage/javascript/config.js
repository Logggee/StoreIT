function generateCollumnInputFields(input) {
    // If the user entered a number smaller then 0 or 0 enter the min value
    if (input.value == 1) {
        input.value = 1;
    }
    const numberOfRows = parseInt(input.value);  // Liest den Wert aus dem Inputfeld und konvertiert ihn in eine Zahl
    const container_row = document.getElementById("container-columns"); // Holt den Ziel-Container
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
        inputField.placeholder = "0";
        inputField.min = "1";
        inputField.oninput = function(){generStorageLayout(this, i+1)};
        
        // Füge die Elemente zum colDiv hinzu
        colDiv.appendChild(label);
        colDiv.appendChild(inputField);
        
        // Füge colDiv dem Haupt-Container hinzu
        container_row.appendChild(colDiv);
    }

    // If the number of rows is decremented the last row needs to be deleted
    const container_storage_layout = document.getElementById("storage-layout-container");
    for (let i = 0; i < container_storage_layout.children.length - numberOfRows; i++) {
        container_storage_layout.removeChild(container_storage_layout.lastChild);
    }
}


function generStorageLayout(input, row_number) {
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
    // Append all rows the the container
    rows.forEach((row) => {
        container_storage_layout.appendChild(row);
    });
}