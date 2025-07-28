document.addEventListener('DOMContentLoaded', function () {

    // --- Smooth Scrolling for Navigation Links ---
    document.querySelectorAll('nav a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            document.querySelector(this.getAttribute('href')).scrollIntoView({
                behavior: 'smooth'
            });
        });
    });

    // --- Animation on Scroll Logic using Intersection Observer ---

    // MODIFIED: Select ALL elements with the .animate-on-scroll class
    const animatedElements = document.querySelectorAll('.animate-on-scroll');

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            // When the element is in view
            if (entry.isIntersecting) {
                // Add the 'visible' class to trigger the CSS transition
                entry.target.classList.add('visible');
                // Stop observing the element so the animation doesn't re-trigger
                observer.unobserve(entry.target);
            }
        });
    }, {
        threshold: 0.1 // Trigger when 10% of the element is visible
    });

    // Observe each of the elements
    animatedElements.forEach(el => {
        observer.observe(el);
    });

});