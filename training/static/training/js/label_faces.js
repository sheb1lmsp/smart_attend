// Initialize Select2 for dropdowns
$(document).ready(function() {
    $('.student-select').select2({
        placeholder: "",
        allowClear: true,
        width: '100%',
        dropdownCssClass: 'custom-select2-dropdown'
    });

    // Handle selection change
    $('.student-select').on('change', function() {
        const faceItem = $(this).closest('.face-item');
        const clearBtn = faceItem.find('.clear-btn');
        if ($(this).val()) {
            faceItem.addClass('selected');
            clearBtn.show();
        } else {
            faceItem.removeClass('selected');
            clearBtn.hide();
        }
    });

    // Initialize clear buttons visibility
    $('.student-select').each(function() {
        const faceItem = $(this).closest('.face-item');
        const clearBtn = faceItem.find('.clear-btn');
        if ($(this).val()) {
            faceItem.addClass('selected');
            clearBtn.show();
        } else {
            clearBtn.hide();
        }
    });

    // Clear selection on button click
    $('.clear-btn').on('click', function() {
        const faceItem = $(this).closest('.face-item');
        const select = faceItem.find('.student-select');
        select.val('').trigger('change');
        faceItem.removeClass('selected');
        $(this).hide();
    });

    // Form submission with loading spinner
    $('#labelForm').on('submit', function() {
        const submitBtn = $('#submitBtn');
        const spinner = $('#spinner');
        submitBtn.prop('disabled', true);
        submitBtn.find('i').removeClass('bi-check-circle').addClass('bi-hourglass-split');
        spinner.show();
    });

    // Enable Bootstrap tooltips
    const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]');
    const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl));

    // Add ripple effect to buttons
    document.querySelectorAll('.btn-custom, .clear-btn').forEach(button => {
        button.addEventListener('click', (e) => {
            const rect = button.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;

            const ripple = document.createElement('span');
            ripple.style.position = 'absolute';
            ripple.style.background = 'rgba(255, 255, 255, 0.3)';
            ripple.style.borderRadius = '50%';
            ripple.style.transform = 'translate(-50%, -50%)';
            ripple.style.width = '100px';
            ripple.style.height = '100px';
            ripple.style.left = `${x}px`;
            ripple.style.top = `${y}px`;
            ripple.style.animation = 'ripple 0.6s linear';
            button.appendChild(ripple);

            setTimeout(() => ripple.remove(), 600);
        });
    });

    // Add style for ripple effect
    const style = document.createElement('style');
    style.innerHTML = `
        @keyframes ripple {
            to {
                transform: translate(-50%, -50%) scale(2);
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
});