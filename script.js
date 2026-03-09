document.addEventListener("DOMContentLoaded", () => {

    // 1. Ambient Cursor Glow
    const glow = document.getElementById('ambient-glow');

    document.addEventListener('mousemove', (e) => {
        // Move the 600x600 glow element to be centered exactly on cursor
        const x = e.clientX - 300;
        const y = e.clientY - 300;

        glow.style.transform = `translate(${x}px, ${y}px)`;

        // Show glow only when mouse moves
        if (glow.style.opacity !== '1') {
            glow.style.opacity = '1';
        }
    });

    document.addEventListener('mouseleave', () => {
        glow.style.opacity = '0';
    });


    // 2. Intersection Observer for Scroll Reveals
    const revealElements = document.querySelectorAll('.scroll-fade-up');

    // Very slight offset margin to trigger when 10% visible
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
                // Stop observing once revealed to retain state
                observer.unobserve(entry.target);
            }
        });
    }, {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    });

    revealElements.forEach(el => observer.observe(el));


    // 3. Smooth Auto-Scroll for Navigation
    document.querySelectorAll('.nav-links a[href^="#"], .hero-actions a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            const targetEl = document.querySelector(targetId);

            if (targetEl) {
                targetEl.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // 4. Parallax Scroll Effect
    const parallaxElements = document.querySelectorAll('.parallax-slow, .parallax-element');

    window.addEventListener('scroll', () => {
        const scrolled = window.scrollY;

        parallaxElements.forEach(el => {
            // Calculate a gentle transform based on scroll depth
            const speed = 0.12; // slow parallax factor
            el.style.transform = `translateY(${scrolled * speed}px)`;
        });
    });


    // 5. Form Submission Logic
    const form = document.getElementById('auditForm');
    if (form) {
        form.addEventListener('submit', async (e) => {
            e.preventDefault();

            const btn = form.querySelector('button');
            const originalText = btn.innerText;

            // Interaction Feedback
            btn.innerHTML = 'Transmitting Data...';
            btn.style.opacity = '0.7';

            const name = document.getElementById('formName').value;
            const email = document.getElementById('formEmail').value;
            const issue = document.getElementById('formIssue').value;

            try {
                // Post to Web3Forms Serverless API
                const response = await fetch('https://api.web3forms.com/submit', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Accept': 'application/json'
                    },
                    body: JSON.stringify({
                        access_key: '2e0af9a9-f277-49fa-a5fc-f0a928d786e0',
                        name: name,
                        email: email,
                        message: issue,
                        subject: 'New Operational Audit Request - NexGen Agency'
                    })
                });

                const result = await response.json();

                if (response.ok) {
                    btn.innerHTML = 'Audit Request Received <span class="text-cyan">✓</span>';
                    btn.style.background = '#06b6d4'; // Flash the cyan color
                    btn.style.color = '#000000';
                    btn.style.opacity = '1';
                    form.reset();
                } else {
                    btn.innerText = 'Error Connection Failed';
                    btn.style.background = '#ef4444';
                }
            } catch (err) {
                btn.innerText = 'Network Error';
                btn.style.background = '#ef4444';
            }

            // Revert state after a few seconds
            setTimeout(() => {
                btn.innerHTML = originalText;
                btn.style.background = ''; // reset to CSS defined
                btn.style.color = '';
                btn.style.opacity = '1';
            }, 4500);
        });
    }
});
