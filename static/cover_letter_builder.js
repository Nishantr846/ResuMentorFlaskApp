document.addEventListener('DOMContentLoaded', () => {
    const generateBtn = document.getElementById('generate-letter-btn');
    const resumeUploadInput = document.getElementById('resume-upload');
    const letterOutputDiv = document.getElementById('letter-output');
    const outputActionsDiv = document.getElementById('output-actions');
    const copyBtn = document.getElementById('copy-btn');
    const jobDescInput = document.getElementById('job-description');

    // Get new elements for file display
    const uploadBox = document.getElementById('upload-box');
    const uploadPrompt = document.getElementById('upload-prompt-cl');
    const fileDisplay = document.getElementById('file-display-cl');
    const fileNameDisplay = document.getElementById('file-name-display-cl');

    // --- FILE SELECTION AND DISPLAY LOGIC ---
    const handleFileSelect = (file) => {
        if (!file) return;
        
        // Update UI to show the selected file's name
        uploadPrompt.style.display = 'none';
        fileNameDisplay.textContent = file.name;
        fileDisplay.style.display = 'block';
    };

    resumeUploadInput.addEventListener('change', (e) => handleFileSelect(e.target.files[0]));
    
    // Drag and drop events
    uploadBox.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadBox.classList.add('dragover'); // You can add a 'dragover' style in CSS if you like
    });
    uploadBox.addEventListener('dragleave', () => {
        uploadBox.classList.remove('dragover');
    });
    uploadBox.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadBox.classList.remove('dragover');
        handleFileSelect(e.dataTransfer.files[0]);
    });


    // --- GENERATE LETTER BUTTON LOGIC ---
    generateBtn.addEventListener('click', async () => {
        const jobDescription = jobDescInput.value;
        const resumeFile = resumeUploadInput.files[0];

        // Validation
        if (!jobDescription.trim()) {
            alert('Please paste a job description.');
            return;
        }
        if (!resumeFile) {
            alert('Please upload your resume file.');
            return;
        }

        // Update UI to show loading state
        generateBtn.textContent = 'Generating...';
        generateBtn.disabled = true;
        letterOutputDiv.innerHTML = `<div class="spinner"></div> <p>AI is crafting your letter...</p>`;
        outputActionsDiv.style.display = 'none';

        // Prepare data and send to backend
        const formData = new FormData();
        formData.append('job_description', jobDescription);
        formData.append('resume', resumeFile);

        try {
            const response = await fetch('/build_cover_letter', {
                method: 'POST',
                body: formData
            });

            const data = await response.json();

            if (data.success) {
                letterOutputDiv.innerHTML = `<textarea>${data.cover_letter_text}</textarea>`;
                outputActionsDiv.style.display = 'flex';
            } else {
                letterOutputDiv.innerHTML = `<div class="error-message">${data.message}</div>`;
            }

        } catch (error) {
            console.error('Error:', error);
            letterOutputDiv.innerHTML = `<div class="error-message">An unexpected error occurred. Please try again.</div>`;
        } finally {
            generateBtn.textContent = 'Generate Cover Letter';
            generateBtn.disabled = false;
        }
    });

    // Copy to clipboard functionality
    copyBtn.addEventListener('click', () => {
        const letterText = letterOutputDiv.querySelector('textarea');
        if (letterText) {
            letterText.select();
            document.execCommand('copy');
            alert('Copied to clipboard!');
        }
    });
});