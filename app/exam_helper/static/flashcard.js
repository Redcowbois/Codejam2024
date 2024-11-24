document.addEventListener('DOMContentLoaded', function () {
    fetch('', {
        method: 'POST', // Use POST if you need to send data to the backend
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify("test"),
    })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json(); // Assuming the backend returns JSON
        })
        .then(data => {
            console.log('Data fetched successfully:', data);
            const container = document.getElementById('page-content')
            container.innerHTML(`<p>${data.message}</p>`)
        })
        .catch(error => {
            console.error('There was a problem with the fetch operation:', error);
        });
}, false);