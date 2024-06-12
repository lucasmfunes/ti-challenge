document.addEventListener('DOMContentLoaded', function() {
    loadProcessSelector();
});

function loadProcessSelector() {
    fetch('http://localhost:5000/api/process_header')
        .then(response => response.json())
        .then(data => {
            const selector = document.getElementById('process-selector');
            data.forEach(process => {
                if (process[1].includes('summary')) { 
                    const option = document.createElement('option');
                    option.value = process[0];  
                    option.textContent = `${process[2]} - ${process[1]}`;  
                    selector.appendChild(option);
                }
            });
        })
        .catch(error => console.error('Error loading process header:', error));
}

function loadSummaryData() {
    const processId = document.getElementById('process-selector').value;
    fetchData(`http://localhost:5000/api/register_data?process_id=${processId}`, 'register-data-table');
    fetchData(`http://localhost:5000/api/gender_data?process_id=${processId}`, 'gender-data-table');
    fetchData(`http://localhost:5000/api/age_data?process_id=${processId}`, 'age-data-table');
    fetchData(`http://localhost:5000/api/city_data?process_id=${processId}`, 'city-data-table');
    fetchData(`http://localhost:5000/api/os_data?process_id=${processId}`, 'os-data-table');

    loadCharts(processId);
}

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

function loadCharts(processId) {
    fetch(`http://localhost:5000/api/gender_data?process_id=${processId}`)
        .then(response => response.json())
        .then(data => {
            console.log('Gender Data:', data); 
            const ctx = document.getElementById('gender-chart').getContext('2d');
            const labels = data.map(d => d[2]);  
            const chartData = data.map(d => d[3]);  
            new Chart(ctx, {
                type: 'pie',
                data: {
                    labels: labels,
                    datasets: [{
                        label: 'Gender Distribution',
                        data: chartData,
                        backgroundColor: ['red', 'blue', 'green']
                    }]
                }
            });
        })
        .catch(error => console.error('Error loading gender chart:', error));

    fetch(`http://localhost:5000/api/os_data?process_id=${processId}`)
        .then(response => response.json())
        .then(data => {
            console.log('OS Data:', data);  
            const ctx = document.getElementById('os-chart').getContext('2d');
            const labels = data.map(d => d[2]);  
            const chartData = data.map(d => d[3]); 
            new Chart(ctx, {
                type: 'pie',
                data: {
                    labels: labels,
                    datasets: [{
                        label: 'OS Distribution',
                        data: chartData,
                        backgroundColor: ['yellow', 'gray', 'black']
                    }]
                }
            });
        })
        .catch(error => console.error('Error loading OS chart:', error));
}
