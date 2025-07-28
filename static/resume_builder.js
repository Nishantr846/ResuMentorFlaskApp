document.addEventListener('DOMContentLoaded', () => {
    const templateCards = document.querySelectorAll('.template-card');
    const resumeForm = document.getElementById('resume-form');
    const addExperienceBtn = document.getElementById('add-experience');
    const addEducationBtn = document.getElementById('add-education');
    const addSocialLinkBtn = document.getElementById('add-social-link');
    const socialLinksContainer = document.getElementById('social-links-container');
    
    const modal = document.getElementById('preview-modal');
    const modalImg = document.getElementById('modal-image');
    const closeBtn = document.querySelector('.close-button');

    let experienceCount = 1;
    let educationCount = 1;
    let socialLinkCount = 1;

    templateCards.forEach(card => {
        card.addEventListener('click', () => {
            modal.style.display = "block";
            modalImg.src = card.querySelector('img').src;
            templateCards.forEach(c => c.classList.remove('selected'));
            card.classList.add('selected');
        });
    });

    const closeModal = () => {
        modal.style.display = "none";
        resumeForm.style.display = 'block';
        resumeForm.scrollIntoView({ behavior: 'smooth' });
    };

    closeBtn.addEventListener('click', closeModal);
    window.addEventListener('click', (event) => {
        if (event.target == modal) {
            closeModal();
        }
    });

    // Add More Social Links (with new structure)
    addSocialLinkBtn.addEventListener('click', () => {
        socialLinkCount++;
        const newEntry = document.createElement('div');
        newEntry.classList.add('social-link-entry');
        
        // This creates a wrapper for the input and button for proper positioning
        newEntry.innerHTML = `
            <div class="input-wrapper">
                <input type="url" name="social_link_${socialLinkCount}" placeholder="GitHub, Portfolio, etc.">
                <button type="button" class="delete-link-btn">&times;</button>
            </div>
        `;
        socialLinksContainer.appendChild(newEntry);
    });

    // Logic to handle deleting a social link
    socialLinksContainer.addEventListener('click', (event) => {
        if (event.target.classList.contains('delete-link-btn')) {
            event.target.closest('.social-link-entry').remove();
        }
    });
    
    // Add More Experience
    addExperienceBtn.addEventListener('click', () => {
        experienceCount++;
        const experienceFields = document.getElementById('experience-fields');
        const newEntry = document.createElement('div');
        newEntry.classList.add('experience-entry');
        newEntry.innerHTML = `
            <hr style="margin-bottom: 1rem;">
            <input type="text" name="experience_title_${experienceCount}" placeholder="Job Title">
            <input type="text" name="experience_company_${experienceCount}" placeholder="Company">
            <input type="text" name="experience_dates_${experienceCount}" placeholder="Dates (e.g., Jan 2020 - Present)">
            <textarea name="experience_desc_${experienceCount}" placeholder="Key Responsibilities and Achievements..."></textarea>
        `;
        experienceFields.appendChild(newEntry);
    });
    
    // Add More Education
    addEducationBtn.addEventListener('click', () => {
        educationCount++;
        const educationFields = document.getElementById('education-fields');
        const newEntry = document.createElement('div');
        newEntry.classList.add('education-entry');
        newEntry.innerHTML = `
            <hr style="margin-bottom: 1rem;">
            <input type="text" name="education_degree_${educationCount}" placeholder="Degree or Certificate">
            <input type="text" name="education_school_${educationCount}" placeholder="School or University">
            <input type="text" name="education_dates_${educationCount}" placeholder="Dates (e.g., Aug 2016 - May 2020)">
            <input type="text" name="education_marks_${educationCount}" placeholder="GPA or Percentage (e.g., 3.8/4.0)">
        `;
        educationFields.appendChild(newEntry);
    });

    // Form Submission
    resumeForm.addEventListener('submit', (e) => {
        e.preventDefault();
        alert('Resume generated! (Download functionality would be implemented here)');
    });
});