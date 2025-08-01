document.addEventListener('DOMContentLoaded', function() {
    // --- Element selection (no changes) ---
    const uploadSection = document.getElementById('upload-section');
    const loadingSection = document.getElementById('loading-section');
    const resultsSection = document.getElementById('results-section');
    const fileInput = document.getElementById('resume-upload');
    const dropZone = document.getElementById('drop-zone');
    const uploadPrompt = document.getElementById('upload-prompt');
    const fileDisplay = document.getElementById('file-display');
    const fileNameDisplay = document.getElementById('file-name-display');
    const analyzeButton = document.getElementById('analyze-button');

    let selectedFile = null;

    // --- File selection logic (no changes) ---
    const handleFileSelect = (file) => {
        if (!file) return;
        selectedFile = file;
        uploadPrompt.style.display = 'none';
        fileNameDisplay.textContent = file.name;
        fileDisplay.style.display = 'block';
        analyzeButton.style.display = 'inline-block';
    };

    fileInput.addEventListener('change', (e) => handleFileSelect(e.target.files[0]));
    dropZone.addEventListener('dragover', (e) => { e.preventDefault(); dropZone.classList.add('dragover'); });
    dropZone.addEventListener('dragleave', () => dropZone.classList.remove('dragover'));
    dropZone.addEventListener('drop', (e) => {
        e.preventDefault();
        dropZone.classList.remove('dragover');
        handleFileSelect(e.dataTransfer.files[0]);
    });

    // --- MODIFIED: Backend communication on button click ---
    analyzeButton.addEventListener('click', () => {
        if (selectedFile) {
            handleFileUpload(selectedFile);
        } else {
            alert("Please select a file first.");
        }
    });

    async function handleFileUpload(file) {
        uploadSection.style.display = 'none';
        loadingSection.style.display = 'block';
        resultsSection.style.display = 'none';

        const formData = new FormData();
        formData.append('resume', file);
        
        // ADDED: Append question counts to the form data
        formData.append('tech_count', document.getElementById('tech-questions').value);
        formData.append('behavioral_count', document.getElementById('behavioral-questions').value);
        formData.append('design_count', document.getElementById('design-questions').value);

        try {
            const response = await fetch('/upload_resume', {
                method: 'POST',
                body: formData
            });
            const data = await response.json();
            
            loadingSection.style.display = 'none';
            if (data.success) {
                displayResults(data.results);
            } else {
                displayError(data.message);
            }
        } catch (error) {
            loadingSection.style.display = 'none';
            displayError('An unexpected error occurred. Please ensure the server is running and try again.');
            console.error('Error:', error);
        }
    }

    // --- DISPLAY RESULTS LOGIC (no changes here) ---

    function displayResults(results) {
    const resultsHTML = `
        <div class="tabs">
            <button class="tab-link active" onclick="openTab(event, 'Feedback')">Resume Feedback</button>
            <button class="tab-link" onclick="openTab(event, 'Jobs')">Job Matches</button>
            <button class="tab-link" onclick="openTab(event, 'Interview')">Interview Prep</button>
        </div>
        <div id="Feedback" class="tab-content" style="display:block;">
            ${results.resume_feedback || '<p>No feedback available.</p>'}
        </div>
        <div id="Jobs" class="tab-content">
            ${results.job_matches || '<p>No job matches available.</p>'}
        </div>
        <div id="Interview" class="tab-content">
            ${results.interview_prep || '<p>No interview prep available.</p>'}
        </div>
    `;
    
        // Display the main results content
        resultsSection.innerHTML = resultsHTML;
        resultsSection.style.display = 'block';

        // --- NEW: Create and add the "Analyze Another Resume" button ---
        const analyzeAnotherButton = document.createElement('button');
        analyzeAnotherButton.id = 'analyze-another-button';
        analyzeAnotherButton.className = 'cta-button'; // Use your existing class for styling
        analyzeAnotherButton.textContent = 'Analyze Another Resume';
        analyzeAnotherButton.style.marginTop = '2rem'; // Add some space above the button
    
        // Add the functionality to reload the page when clicked
        analyzeAnotherButton.onclick = function() {
            window.location.reload();
            };
            
        // Add the button to the bottom of the results section
        resultsSection.appendChild(analyzeAnotherButton);
        }
    
    function displayError(message) {
        resultsSection.innerHTML = `<div class="error-message">${message}</div>`;
        resultsSection.style.display = 'block';
    }
});

// --- GLOBAL TAB SWITCHING LOGIC (no changes here) ---

function openTab(evt, tabName) {
    const tabcontent = document.getElementsByClassName("tab-content");
    for (let i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
    }
    const tablinks = document.getElementsByClassName("tab-link");
    for (let i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" active", "");
    }
    document.getElementById(tabName).style.display = "block";
    evt.currentTarget.className += " active";
}