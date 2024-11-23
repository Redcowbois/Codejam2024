// JavaScript code for file upload and preview functionality

// Retrieve file details from localStorage
const fileData = JSON.parse(localStorage.getItem('uploadedFile'));

if (fileData) {
    // Display file metadata
    document.getElementById('file-name').textContent = `File Name: ${fileData.name}`;
    document.getElementById('file-type').textContent = `File Type: ${fileData.type}`;
    document.getElementById('file-size').textContent = `File Size: ${(fileData.size / 1024).toFixed(2)} KB`;

    // Display file content or placeholder
    const fileContent = document.getElementById('file-content');

    if (fileData.type === 'text/plain') {
        // Display text file content
        const text = atob(fileData.content.split(',')[1]);
        fileContent.textContent = text;
    } else if (fileData.type === 'application/pdf') {
        // Display PDF file as an embed
        const pdfEmbed = document.createElement('embed');
        pdfEmbed.src = fileData.content;
        pdfEmbed.type = 'application/pdf';
        pdfEmbed.width = '100%';
        pdfEmbed.height = '400px';
        fileContent.appendChild(pdfEmbed);
    } else if (fileData.type === 'video/mp4') {
        // Display MP4 file as a video element
        const video = document.createElement('video');
        video.src = fileData.content; // The base64 data URL for the video
        video.width = 640; // Set appropriate width for video
        video.height = 360; // Set appropriate height for video
        video.controls = true; // Add video controls (play, pause, etc.)
        video.autoplay = true; // Autoplay the video
        video.muted = true; // Mute the video to allow autoplay without user interaction
        fileContent.appendChild(video);
    } else {
        fileContent.textContent = 'Preview is not available for this file type.';
    }
}

// Handle options
function chooseOption(action) {
    alert(`Redirecting to ${action} functionality!`);
}

// Return to the previous page
function goBack() {
    window.history.back();
}

// File upload and form submission handling
document.getElementById('file-upload').addEventListener('change', function () {
    const fileDisplay = document.getElementById('file-display');
    const file = this.files[0];
    if (file) {
        fileDisplay.textContent = file.name;
    } else {
        fileDisplay.textContent = 'No file chosen';
    }
});

document.getElementById('upload-form').addEventListener('submit', function (event) {
    event.preventDefault(); // Prevent form from refreshing the page

    const fileInput = document.getElementById('file-upload');
    const message = document.getElementById('message');

    if (!fileInput.files.length) {
        message.textContent = 'Please upload a file.';
        return;
    }

    const file = fileInput.files[0];
    const allowedExtensions = ['pdf', 'mp4', 'txt'];
    const fileExtension = file.name.split('.').pop().toLowerCase();

    if (!allowedExtensions.includes(fileExtension)) {
        message.textContent = 'Invalid file type. Only PDF, MP4, and TXT files are allowed.';
        return;
    }

    // Save file details to localStorage
    const reader = new FileReader();
    reader.onload = function () {
        localStorage.setItem('uploadedFile', JSON.stringify({
            name: file.name,
            type: file.type,
            size: file.size,
            content: reader.result // Save base64 content for MP4, PDF, and TXT
        }));
        window.location.href = 'file-options.html'; // Redirect to File Options Page
    };
    reader.readAsDataURL(file);
});
