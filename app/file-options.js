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
        pdfEmbed.height = '500px';
        fileContent.appendChild(pdfEmbed);
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
