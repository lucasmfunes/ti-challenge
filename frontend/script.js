document.addEventListener('DOMContentLoaded', function() {
    fetchData('http://localhost:5000/api/process_header', 'process-header-table');
    fetchData('http://localhost:5000/api/etl_data', 'etl-data-table');
    fetchData('http://localhost:5000/api/summary_data', 'summary-data-table');
});

function fetchData(endpoint, tableId) {
    fetch(endpoint)
        .then(response => response.json())
        .then(data => {
            populateTable(data, tableId);
        })
        .catch(error => console.error('Error fetching data:', error));
}

function populateTable(data, tableId) {
    const tableBody = document.querySelector(`#${tableId} tbody`);
    tableBody.innerHTML = '';

    data.forEach(row => {
        const tr = document.createElement('tr');
        Object.values(row).forEach(cell => {
            const td = document.createElement('td');
            td.textContent = cell;
            tr.appendChild(td);
        });
        tableBody.appendChild(tr);
    });
}
