window.onload = function() {
    // Create data to send in the request body
    const data = {
        key: 'value', // Your data here
        another_key: 'another_value'
    };

    // Use fetch API to send a POST request
    fetch('', {
        method: 'POST', // HTTP method
        headers: {
            'Content-Type': 'application/json', // Sending JSON
        },
        body: JSON.stringify(data) // Convert JavaScript object to JSON string
    })
    .then(response => response.json()) // Parse JSON response
    .then(data => {
        console.log('Success:', data); // Handle the response from Django
        var audioSource = document.getElementById('audio-source'); // Get the source element
        audioSource.src = '/static/podcast.mp3';
        var audioElement = audioSource.parentElement;
        audioElement.load(); // This reloads the audio element with the new source
            
            // Optionally, start playing the new audio
        audioElement.play();
    })
    .catch((error) => {
        console.error('Error:', error); // Handle errors
    });
};