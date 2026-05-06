document.addEventListener('DOMContentLoaded', function() {

    // ── Dark mode toggle ──────────────────────────────────────────────────────
    const darkModeToggle = document.getElementById('darkModeToggle');
    const darkModeStylesheet = document.getElementById('dark-mode-stylesheet');

    function setDarkMode(enabled) {
        if (enabled) {
            document.body.classList.add('dark-mode');
            if (darkModeStylesheet) darkModeStylesheet.disabled = false;
            document.cookie = "darkMode=true; path=/; max-age=31536000";
            if (darkModeToggle) darkModeToggle.innerHTML = '<i class="fas fa-sun"></i>';
        } else {
            document.body.classList.remove('dark-mode');
            if (darkModeStylesheet) darkModeStylesheet.disabled = true;
            document.cookie = "darkMode=false; path=/; max-age=31536000";
            if (darkModeToggle) darkModeToggle.innerHTML = '<i class="fas fa-moon"></i>';
        }
    }

    if (darkModeToggle) {
        darkModeToggle.addEventListener('click', function() {
            setDarkMode(!document.body.classList.contains('dark-mode'));
        });
    }

    const darkModeCookie = document.cookie.split('; ').find(row => row.startsWith('darkMode='));
    if (darkModeCookie) {
        const isDark = darkModeCookie.split('=')[1] === 'true';
        setDarkMode(isDark);
    }

    // ── Download toast ────────────────────────────────────────────────────────
    window.showDownloadToast = function(message) {
        let container = document.getElementById('toastContainer');
        if (!container) {
            container = document.createElement('div');
            container.id = 'toastContainer';
            container.className = 'toast-container position-fixed bottom-0 end-0 p-3';
            document.body.appendChild(container);
        }
        const toastEl = document.createElement('div');
        toastEl.className = 'toast align-items-center text-bg-success border-0 rounded-4';
        toastEl.setAttribute('role', 'alert');
        toastEl.innerHTML = `
            <div class="d-flex">
                <div class="toast-body"><i class="fas fa-check-circle me-2"></i>${message}</div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
            </div>`;
        container.appendChild(toastEl);
        const toast = new bootstrap.Toast(toastEl, { delay: 3000 });
        toast.show();
        toastEl.addEventListener('hidden.bs.toast', () => toastEl.remove());
    };

    // ── PDF preview modal ─────────────────────────────────────────────────────
    window.previewPDF = function(url) {
        const modalEl = document.getElementById('pdfModal');
        const iframe = document.getElementById('pdfIframe');
        const fallback = document.getElementById('pdfFallbackLink');
        const fullUrl = url.startsWith('/') ? window.location.origin + url : url;
        iframe.src = fullUrl;
        if (fallback) fallback.href = fullUrl;
        const modal = new bootstrap.Modal(modalEl);
        modal.show();
        modalEl.addEventListener('hidden.bs.modal', () => { iframe.src = ''; }, { once: true });
    };

    // ── Particle explosion on click ───────────────────────────────────────────
    document.addEventListener('click', function(e) {
        if (e.target.closest('a, button, input, select, textarea')) return;
        const colors = [
            '#ff3333','#ff9933','#ffff33','#33ff33','#33ffff',
            '#3399ff','#9933ff','#ff33ff','#ff3399','#ffcc00'
        ];
        const particles = [];
        for (let i = 0; i < 20; i++) {
            const p = document.createElement('div');
            p.className = 'particle';
            p.style.left = e.clientX + 'px';
            p.style.top = e.clientY + 'px';
            const size = Math.random() * 6 + 2;
            p.style.width = size + 'px';
            p.style.height = size + 'px';
            const color = colors[Math.floor(Math.random() * colors.length)];
            p.style.background = color;
            p.style.boxShadow = `0 0 6px ${color}`;
            p.dataset.angle = Math.random() * Math.PI * 2;
            p.dataset.speed = Math.random() * 150 + 50;
            p.dataset.startTime = performance.now();
            document.body.appendChild(p);
            particles.push(p);
        }
        const lifetime = 800;
        function animate() {
            const now = performance.now();
            for (let i = particles.length - 1; i >= 0; i--) {
                const p = particles[i];
                const elapsed = now - p.dataset.startTime;
                if (elapsed >= lifetime) { p.remove(); particles.splice(i, 1); continue; }
                const dist = (elapsed / 1000) * parseFloat(p.dataset.speed);
                const dx = Math.cos(p.dataset.angle) * dist;
                const dy = Math.sin(p.dataset.angle) * dist;
                p.style.transform = `translate(calc(-50% + ${dx}px), calc(-50% + ${dy}px))`;
                p.style.opacity = 1 - elapsed / lifetime;
            }
            if (particles.length > 0) requestAnimationFrame(animate);
        }
        requestAnimationFrame(animate);
    });

    // ── Smooth scroll for anchor links ────────────────────────────────────────
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            const target = document.querySelector(this.getAttribute('href'));
            if (target) { e.preventDefault(); target.scrollIntoView({ behavior: 'smooth' }); }
        });
    });

    // ── Category tree collapse caret rotation ─────────────────────────────────
    document.querySelectorAll('[data-bs-toggle="collapse"]').forEach(button => {
        const icon = button.querySelector('i');
        if (!icon) return;
        const target = document.querySelector(button.getAttribute('data-bs-target'));
        if (!target) return;
        target.addEventListener('show.bs.collapse', () => {
            icon.classList.replace('fa-chevron-right', 'fa-chevron-down');
        });
        target.addEventListener('hide.bs.collapse', () => {
            icon.classList.replace('fa-chevron-down', 'fa-chevron-right');
        });
    });

    // ── Back to top button ────────────────────────────────────────────────────
    const backToTop = document.getElementById('backToTop');
    if (backToTop) {
        window.addEventListener('scroll', () => {
            backToTop.style.display = window.scrollY > 300 ? 'block' : 'none';
        });
        backToTop.addEventListener('click', () => {
            window.scrollTo({ top: 0, behavior: 'smooth' });
        });
    }

    // ── Navbar scroll shadow ──────────────────────────────────────────────────
    const navbar = document.querySelector('.navbar');
    if (navbar) {
        window.addEventListener('scroll', () => {
            navbar.classList.toggle('navbar-scrolled', window.scrollY > 10);
        });
    }

});
