function generateCollumnInputFields(input) {
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
        inputField.placeholder = "1";
        inputField.min = "1";
        inputField.oninput = function(){generStorageLayout(this, i+1)};
        
        // Füge die Elemente zum colDiv hinzu
        colDiv.appendChild(label);
        colDiv.appendChild(inputField);
        
        // Füge colDiv dem Haupt-Container hinzu
        container_row.appendChild(colDiv);
    }
}


function generStorageLayout(input, row_number) {
    const number_of_bins = parseInt(input.value);
    const container_storage_layout = document.getElementById("storage-layout-container");
    //container_storage_layout.innerHTML = "";

    const div_row = document.createElement("div");
    div_row.className = "row mb-2 align-items-center";

    const span = document.createElement("span");
    span.innerText = "Row " + row_number;
    div_row.appendChild(span);

    const div_col = document.createElement("div");
    div_col.className = "col d-flex justify-content-between mx-4";

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
    container_storage_layout.appendChild(div_row);
}