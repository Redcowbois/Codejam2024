document.getElementById('upload-form').addEventListener('submit', function (event) {
    event.preventDefault(); // Prevent form from refreshing the page
        
    fetch("/trial", {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json', // Inform server of JSON payload

        },
        body: "test value",
    })
    .then((response) => {
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        return response.json();
    })
    .then((data) => {
        console.log('Response from server:', data);
    })
    .catch((error) => {
        console.error('Error:', error.message);
    });

});

