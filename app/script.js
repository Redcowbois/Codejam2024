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

    // Save file details and content to localStorage
    const reader = new FileReader();
    reader.onload = function () {
        localStorage.setItem('uploadedFile', JSON.stringify({
            name: file.name,
            type: file.type,
            size: file.size,
            content: reader.result
        }));
        window.location.href = 'file-options.html'; // Redirect to File Options Page
    };
    reader.readAsDataURL(file);
});
