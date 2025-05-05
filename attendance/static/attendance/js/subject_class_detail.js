// Enable Bootstrap tooltips
const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]');
const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl));

// Sortable columns
document.querySelectorAll('.sortable').forEach(th => {
    th.addEventListener('click', () => {
        const sortKey = th.dataset.sort;
        const isAsc = !th.classList.contains('sort-asc');
        
        document.querySelectorAll('.sortable').forEach(t => {
            t.classList.remove('sort-asc', 'sort-desc');
        });
        th.classList.add(isAsc ? 'sort-asc' : 'sort-desc');

        const tbody = th.closest('table').querySelector('tbody');
        const rows = Array.from(tbody.querySelectorAll('tr:not(.no-data)'));
        const noDataRow = tbody.querySelector('tr.no-data');

        rows.sort((a, b) => {
            const aVal = parseFloat(a.querySelector(`td:nth-last-child(${sortKey === 'total_classes' ? 3 : sortKey === 'present_classes' ? 2 : 1})`).textContent.replace('%', '')) || 0;
            const bVal = parseFloat(b.querySelector(`td:nth-last-child(${sortKey === 'total_classes' ? 3 : sortKey === 'present_classes' ? 2 : 1})`).textContent.replace('%', '')) || 0;
            return isAsc ? aVal - bVal : bVal - aVal;
        });

        tbody.innerHTML = '';
        rows.forEach(row => tbody.appendChild(row));
        if (noDataRow) {
            tbody.appendChild(noDataRow);
        }

        tbody.style.animation = 'fadeInStatus 0.4s';
        setTimeout(() => tbody.style.animation = '', 400);
    });
});

// Add ripple effect to buttons
document.querySelectorAll('.btn-custom').forEach(button => {
    button.addEventListener('click', (e) => {
        const rect = button.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;

        const ripple = document.createElement('span');
        ripple.style.position = 'absolute';
        ripple.style.background = 'rgba(255, 255, 255, 0.4)';
        ripple.style.borderRadius = '50%';
        ripple.style.transform = 'translate(-50%, -50%)';
        ripple.style.width = '120px';
        ripple.style.height = '120px';
        ripple.style.left = `${x}px`;
        ripple.style.top = `${y}px`;
        ripple.style.animation = 'ripple 0.7s linear';
        button.appendChild(ripple);

        setTimeout(() => ripple.remove(), 700);
    });
});

// Animation styles
const style = document.createElement('style');
style.innerHTML = `
    @keyframes fadeInStatus {
        from { opacity: 0.5; }
        to { opacity: 1; }
    }
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