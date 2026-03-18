// Dark mode toggle
document.addEventListener('DOMContentLoaded', function() {
    const darkModeToggle = document.getElementById('darkModeToggle');
    const darkModeStylesheet = document.getElementById('dark-mode-stylesheet');
    
    // Check cookie for dark mode preference
    function setDarkMode(enabled) {
        if (enabled) {
            document.body.classList.add('dark-mode');
            darkModeStylesheet.disabled = false;
            document.cookie = "darkMode=true; path=/";
        } else {
            document.body.classList.remove('dark-mode');
            darkModeStylesheet.disabled = true;
            document.cookie = "darkMode=false; path=/";
        }
    }

    if (darkModeToggle) {
        darkModeToggle.addEventListener('click', function() {
            const isDark = document.body.classList.contains('dark-mode');
            setDarkMode(!isDark);
        });
    }

    // Initialize from cookie
    const darkModeCookie = document.cookie.split('; ').find(row => row.startsWith('darkMode='));
    if (darkModeCookie) {
        const value = darkModeCookie.split('=')[1];
        setDarkMode(value === 'true');
    }

    // Toast for download confirmation
    window.showDownloadToast = function(message) {
        const toastContainer = document.getElementById('toastContainer');
        if (!toastContainer) {
            const container = document.createElement('div');
            container.id = 'toastContainer';
            container.className = 'toast-container position-fixed bottom-0 end-0 p-3';
            document.body.appendChild(container);
        }
        const toastEl = document.createElement('div');
        toastEl.className = 'toast align-items-center text-bg-success border-0';
        toastEl.setAttribute('role', 'alert');
        toastEl.innerHTML = `
            <div class="d-flex">
                <div class="toast-body">${message}</div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
            </div>
        `;
        document.getElementById('toastContainer').appendChild(toastEl);
        const toast = new bootstrap.Toast(toastEl);
        toast.show();
        toastEl.addEventListener('hidden.bs.toast', () => toastEl.remove());
    };

    window.previewPDF = function(url) {
        const modalEl = document.getElementById('pdfModal');
        const iframe = document.getElementById('pdfIframe');
        const fallback = document.getElementById('pdfFallbackLink');

        // Use window.location.origin only if URL is relative
        let fullUrl = url;
        if (url.startsWith('/')) {
            fullUrl = window.location.origin + url;
        }

        iframe.src = fullUrl;
        fallback.href = fullUrl;

        const modal = new bootstrap.Modal(modalEl);
        modal.show();

        // Clear iframe when modal closes
        modalEl.addEventListener('hidden.bs.modal', () => {
            iframe.src = '';
            fallback.href = '';
        }, { once: true });
    };

    // Particle explosion on click
    document.addEventListener('click', function(e) {
        const particleCount = 36; // number of particles
        const colors = [
        '#ff3333', '#ff9933', '#ffff33', '#33ff33', '#33ffff',
        '#3399ff', '#3333ff', '#9933ff', '#ff33ff', '#ff3399',
        '#ff6633', '#ccff33', '#33ff99', '#33ccff', '#6633ff',
        '#cc33ff', '#ff33cc', '#ff3366', '#ffcc00', '#ff9900'
        ];
        const particles = [];
        const lifetime = 1000; // milliseconds

        for (let i = 0; i < particleCount; i++) {
            const particle = document.createElement('div');
            particle.className = 'particle';

            // Position at click point
            particle.style.left = e.clientX + 'px';
            particle.style.top = e.clientY + 'px';

            // Random size between  2px and 8px
            const size = Math.random() * 6 + 2;
            particle.style.width = size + 'px';
            particle.style.height = size + 'px';

            // Random color from palette
            const color = colors[Math.floor(Math.random() * colors.length)];
            particle.style.color = particle.style.background; // for box-shadow
            particle.style.background = color;
            particle.style.boxShadow = `0 0 6px ${color}`;

            // Random direction (angle in radians) and speed
            const angle = Math.random() * Math.PI * 2;
            const speed = Math.random() * 150 + 50; // pixels per second
            const startTime = performance.now();

            // Store data for animation
            particle.dataset.angle = angle;
            particle.dataset.speed = speed;
            particle.dataset.startTime = startTime;

            document.body.appendChild(particle);
            particles.push(particle);
        }

        function animateParticles() {
            const now = performance.now();
            for (let i = particles.length - 1; i >= 0; i--) {
                const p = particles[i];
                const elapsed = now - p.dataset.startTime;

                if (elapsed >= lifetime) {
                    p.remove();
                    particles.splice(i, 1);
                    continue;
                }

                // Calculate position based on elapsed time
                const angle = parseFloat(p.dataset.angle);
                const speed = parseFloat(p.dataset.speed);
                const distance = (elapsed / 1000) * speed; // pixels
                const dx = Math.cos(angle) * distance;
                const dy = Math.sin(angle) * distance;

                // Apply translation relative to center (-50% offset)
                p.style.transform = `translate(calc(-50% + ${dx}px), calc(-50% + ${dy}px))`;

                // Fade out gradually
                const progress = elapsed / lifetime;
                p.style.opacity = 1 - progress;
            }

            if (particles.length > 0) {
                requestAnimationFrame(animateParticles);
            }
        }

        requestAnimationFrame(animateParticles);
    });

    document.querySelectorAll('.list-group a[href^="#program-"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({ behavior: 'smooth' });
            }
        });
    });
    
    document.querySelectorAll('.category-tree li > .toggle').forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            this.parentElement.querySelector('ul').classList.toggle('hidden');
        });
    });

    document.addEventListener('DOMContentLoaded', function() {
        // Rotate caret icon on collapse events
        const collapseButtons = document.querySelectorAll('[data-bs-toggle="collapse"]');
        collapseButtons.forEach(button => {
            const icon = button.querySelector('i');
            if (!icon) return;
            const targetId = button.getAttribute('data-bs-target');
            const target = document.querySelector(targetId);
            if (target) {
                target.addEventListener('show.bs.collapse', function () {
                    icon.classList.remove('fa-chevron-right');
                    icon.classList.add('fa-chevron-down');
                });
                target.addEventListener('hide.bs.collapse', function () {
                    icon.classList.remove('fa-chevron-down');
                    icon.classList.add('fa-chevron-right');
                });
            }
        });
    });

});

