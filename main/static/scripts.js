document.addEventListener('DOMContentLoaded', () => {
    // Handle opening and closing of modals
    const modals = {
        add: document.getElementById('addTruckModal'),
        update: document.getElementById('updateTruckModal'),
        delete: document.getElementById('deleteTruckModal'),
        fetch: document.getElementById('fetchTruckModal')
    };

    const openButtons = {
        add: document.getElementById('openAddModal'),
        update: document.getElementById('openUpdateModal'),
        delete: document.getElementById('openDeleteModal'),
        fetch: document.getElementById('openFetchModal')
    };

    const closeButtons = {
        add: document.getElementById('closeAddModal'),
        update: document.getElementById('closeUpdateModal'),
        delete: document.getElementById('closeDeleteModal'),
        fetch: document.getElementById('closeFetchModal')
    };

    Object.keys(openButtons).forEach(action => {
        openButtons[action].onclick = () => modals[action].style.display = 'block';
        closeButtons[action].onclick = () => modals[action].style.display = 'none';
    });

    window.onclick = (event) => {
        if (event.target.classList.contains('modal')) {
            event.target.style.display = 'none';
        }
    };

    // Handle form submissions
    document.getElementById('addTruckForm').onsubmit = async (event) => {
        event.preventDefault();
        const data = new FormData(event.target);
        const response = await fetch('/api/trucks', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(Object.fromEntries(data))
        });
        const result = await response.json();
        alert(result.message);
        if (result.message === 'Truck added successfully') {
            event.target.reset();
            document.getElementById('addTruckModal').style.display = 'none';
            fetchAllTrucks();
        }
    };

    document.getElementById('updateTruckForm').onsubmit = async (event) => {
        event.preventDefault();
        const data = new FormData(event.target);
        const response = await fetch('/api/trucks', {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(Object.fromEntries(data))
        });
        const result = await response.json();
        alert(result.message);
        if (result.message === 'Truck details updated successfully') {
            event.target.reset();
            document.getElementById('updateTruckModal').style.display = 'none';
            fetchAllTrucks();
        }
    };

    document.getElementById('deleteTruckForm').onsubmit = async (event) => {
        event.preventDefault();
        const data = new FormData(event.target);
        const response = await fetch('/api/trucks', {
            method: 'DELETE',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(Object.fromEntries(data))
        });
        const result = await response.json();
        alert(result.message);
        if (result.message === 'Truck deleted successfully') {
            event.target.reset();
            document.getElementById('deleteTruckModal').style.display = 'none';
            fetchAllTrucks();
        }
    };

    document.getElementById('retrieveTruckForm').onsubmit = async (event) => {
        event.preventDefault();
        const data = new FormData(event.target);
        const truck_id = data.get('truck_id');
        const response = await fetch(`/api/trucks?truck_id=${truck_id}`, {
            method: 'GET',
        });
        const result = await response.json();
        const truckTableBody = document.querySelector('#truckTable tbody');
        truckTableBody.innerHTML = '';
    
        if (result.trucks) {
            const row = truckTableBody.insertRow();
            row.insertCell(0).textContent = result.trucks['TruckID'];
            row.insertCell(1).textContent = result.trucks['Truck Number Plate'];
            row.insertCell(2).textContent = result.trucks['Driver Name'];
            row.insertCell(3).textContent = result.trucks['Driver License ID'];
            row.insertCell(4).textContent = result.trucks['Driver Contact'];
            row.insertCell(5).textContent = result.trucks['Truck RFID'];
        } else {
            truckTableBody.insertRow().insertCell(0).textContent = 'No trucks found';
        }
    
        // Comment this line if you want to keep the modal open
        // document.getElementById('fetchTruckModal').style.display = 'none';
    };
    
    // Example of manually closing the modal
    document.getElementById('closeFetchTruckModal').onclick = () => {
        document.getElementById('fetchTruckModal').style.display = 'none';
    };
    
    const fetchAllTrucks = async () => {
        const response = await fetch('/api/trucks', { method: 'GET' });
        const result = await response.json();
        const truckTableBody = document.querySelector('#truckTable tbody');
        truckTableBody.innerHTML = '';
    
        if (result.trucks) {
            result.trucks.forEach(truck => {
                const row = truckTableBody.insertRow();
                row.insertCell(0).textContent = truck['TruckID'];
                row.insertCell(1).textContent = truck['Truck Number Plate'];
                row.insertCell(2).textContent = truck['Driver Name'];
                row.insertCell(3).textContent = truck['Driver License ID'];
                row.insertCell(4).textContent = truck['Driver Contact'];
                row.insertCell(5).textContent = truck['Truck RFID'];
            });
        }
    };

    fetchAllTrucks();
});

