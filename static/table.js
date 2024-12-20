let dataTable;

function loadTable() {
    const filterColumn = document.getElementById('filter_column').value;
    const filterValue = document.getElementById('filter_value').value;

    // Destroy existing DataTable before creating a new one
    if (dataTable) {
        dataTable.destroy();
    }

    // Fetch filtered data from the server
    fetch('/filtered_data', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: new URLSearchParams({
            'filter_column': filterColumn,
            'filter_value': filterValue,
        }),
    })
    .then(response => response.json())
    .then(data => {
        // Create a DataTable with the filtered data
        dataTable = $('#table-container').DataTable({
            data: data,
            columns: [
                { data: 'name' },
                { data: 'age' },
                { data: 'indoor' },
                { data: 'outdoor' },
            ],
        });
    });
}

function downloadExcel() {
    const filterColumn = document.getElementById('filter_column').value;
    const filterValue = document.getElementById('filter_value').value;

    // Fetch filtered data from the server
    fetch('/download_excel', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: new URLSearchParams({
            'filter_column': filterColumn,
            'filter_value': filterValue,
        }),
    })
    .then(response => response.json())
    .then(data => {
        // Trigger the download of the Excel file
        window.location.href = data.excel_file_path;
    });
}
