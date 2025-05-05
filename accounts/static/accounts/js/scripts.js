// Enable Bootstrap tooltips
const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]');
const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl));

// Add ripple effect to buttons and toggle options
document.querySelectorAll('.btn-custom, .toggle-option').forEach(element => {
    element.addEventListener('click', (e) => {
        const rect = element.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;

        const ripple = document.createElement('span');
        ripple.style.position = 'absolute';
        ripple.style.background = 'rgba(255, 255, 255, 0.4)';
        ripple.style.borderRadius = '50%';
        ripple.style.transform = 'translate(-50%, -50%)';
        ripple.style.width = '100px';
        ripple.style.height = '100px';
        ripple.style.left = `${x}px`;
        ripple.style.top = `${y}px`;
        ripple.style.animation = 'ripple 0.7s linear';
        element.appendChild(ripple);

        setTimeout(() => ripple.remove(), 700);
    });
});

// Toggle user type selection
document.querySelectorAll('.toggle-option').forEach(option => {
    option.addEventListener('click', () => {
        document.querySelectorAll('.toggle-option').forEach(opt => {
            opt.classList.remove('active');
            opt.setAttribute('aria-checked', 'false');
        });
        option.classList.add('active');
        option.setAttribute('aria-checked', 'true');
        document.getElementById('user_type').value = option.dataset.value;
    });

    // Keyboard support
    option.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' || e.key === ' ') {
            e.preventDefault();
            option.click();
        }
    });
});

// Add style for ripple effect
const style = document.createElement('style');
style.innerHTML = `
    @keyframes ripple {
        to {
            transform: translate(-50%, -50%) scale(2.5);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);

// Intersection Observer for fade-in animations
const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('fade-in');
            observer.unobserve(entry.target);
        }
    });
}, { threshold: 0.1 });

document.querySelectorAll('.fade-in').forEach(element => {
    observer.observe(element);
});