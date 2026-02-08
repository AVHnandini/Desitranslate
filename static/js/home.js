// ===========================
// HOME PAGE JAVASCRIPT
// ===========================

document.addEventListener('DOMContentLoaded', function() {
    setupFeatureCards();
});

function setupFeatureCards() {
    const featureCards = document.querySelectorAll('.feature-card');
    
    featureCards.forEach((card, index) => {
        // Add staggered animation
        card.style.animation = `slideUp 0.6s ease-out ${index * 0.1}s both`;
        
        // Add hover effect with sound
        card.addEventListener('mouseenter', function() {
            playHoverSound();
        });
    });
}

function playHoverSound() {
    // Optional: Add audio feedback for better UX
    // This is commented out as it requires audio file
    // const audio = new Audio('/static/sounds/hover.mp3');
    // audio.play().catch(e => console.log('Audio play failed'));
}

// Add intersection observer for scroll animations
if ('IntersectionObserver' in window) {
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, {
        threshold: 0.1
    });
    
    document.querySelectorAll('.step, .feature-card').forEach(element => {
        element.style.opacity = '0';
        element.style.transform = 'translateY(20px)';
        element.style.transition = 'all 0.6s ease-out';
        observer.observe(element);
    });
}
