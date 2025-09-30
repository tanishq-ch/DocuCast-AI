// /static/js/main.js

document.addEventListener("DOMContentLoaded", function() {

    // Fade-in animation for elements with the .fade-in class
    const fadeInElements = document.querySelectorAll('.fade-in');
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.animation = `fadeInAnimation 0.8s ${entry.target.dataset.delay || '0s'} ease-out forwards`;
            }
        });
    }, {
        threshold: 0.1
    });

    fadeInElements.forEach(el => {
        observer.observe(el);
    });

    // Custom file upload handler
    const fileInput = document.getElementById('file-upload');
    const fileUploadName = document.getElementById('file-upload-filename');

    if (fileInput && fileUploadName) {
        fileInput.addEventListener('change', function() {
            if (this.files && this.files.length > 0) {
                fileUploadName.textContent = this.files[0].name;
            } else {
                fileUploadName.textContent = '';
            }
        });
    }

});