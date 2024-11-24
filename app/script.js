
let isDefaultBackground = true;
function toggleBackground() {
      if (isDefaultBackground) {
        // Switch to the new background
        document.body.style.backgroundImage = "url('light2.jpg')";

      } else {
        // Switch back to the default background
        document.body.style.backgroundImage = "url('wallpaperflare.com_wallpaper.jpg')";

      }
      // Toggle the state
      isDefaultBackground = !isDefaultBackground;
    }



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
    if (fileExtension === 'mp4') {
        // For large files like MP4, only save metadata, not content
        localStorage.setItem('uploadedFile', JSON.stringify({
            name: file.name,
            type: file.type,
            size: file.size
        }));
        window.location.href = 'file-options.html'; // Redirect to File Options Page
    } else {
        // For smaller files like PDF and TXT, save the file content
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
    }
});



