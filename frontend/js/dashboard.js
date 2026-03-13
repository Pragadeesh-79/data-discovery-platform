/* ═══════════════════════════════════════════════════════════════
   Cipher — Dashboard Interactions & Animations
   ═══════════════════════════════════════════════════════════════ */

document.addEventListener('DOMContentLoaded', () => {

  // ── Navbar Scroll Effect ──
  const navbar = document.getElementById('navbar');
  if (navbar) {
    window.addEventListener('scroll', () => {
      navbar.classList.toggle('scrolled', window.scrollY > 40);
    });
  }

  // ── Mobile Menu Toggle ──
  const mobileToggle = document.getElementById('mobileToggle');
  const navLinks = document.getElementById('navLinks');
  if (mobileToggle && navLinks) {
    mobileToggle.addEventListener('click', () => {
      navLinks.classList.toggle('open');
      const icon = mobileToggle.querySelector('i');
      icon.classList.toggle('fa-bars');
      icon.classList.toggle('fa-xmark');
    });

    navLinks.querySelectorAll('a').forEach(link => {
      link.addEventListener('click', () => {
        navLinks.classList.remove('open');
        const icon = mobileToggle.querySelector('i');
        icon.classList.add('fa-bars');
        icon.classList.remove('fa-xmark');
      });
    });
  }

  // ── Smooth Scroll ──
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', e => {
      const target = document.querySelector(anchor.getAttribute('href'));
      if (target) {
        e.preventDefault();
        target.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    });
  });

  // ── Scroll Reveal (Intersection Observer) ──
  const revealElements = document.querySelectorAll('.reveal');
  if (revealElements.length > 0) {
    const revealObserver = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('visible');
          revealObserver.unobserve(entry.target);
        }
      });
    }, {
      threshold: 0.1,
      rootMargin: '0px 0px -50px 0px'
    });

    revealElements.forEach((el, i) => {
      el.style.transitionDelay = `${i % 4 * 0.1}s`;
      revealObserver.observe(el);
    });
  }

  // ── Counter Animation ──
  const counters = document.querySelectorAll('[data-count]');
  if (counters.length > 0) {
    const counterObserver = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          animateCounter(entry.target);
          counterObserver.unobserve(entry.target);
        }
      });
    }, { threshold: 0.5 });

    counters.forEach(counter => counterObserver.observe(counter));
  }

  function animateCounter(el) {
    const target = parseInt(el.dataset.count);
    const duration = 2000;
    const start = performance.now();

    function update(now) {
      const elapsed = now - start;
      const progress = Math.min(elapsed / duration, 1);
      // Ease-out
      const eased = 1 - Math.pow(1 - progress, 3);
      const current = Math.floor(eased * target);

      el.textContent = current.toLocaleString();

      if (progress < 1) {
        requestAnimationFrame(update);
      } else {
        el.textContent = target.toLocaleString();
      }
    }

    requestAnimationFrame(update);
  }

  // ── FAQ Accordion ──
  const faqItems = document.querySelectorAll('.faq-item');
  faqItems.forEach(item => {
    const question = item.querySelector('.faq-question');
    if (question) {
      question.addEventListener('click', () => {
        const isActive = item.classList.contains('active');

        // Close all
        faqItems.forEach(i => i.classList.remove('active'));

        // Toggle current
        if (!isActive) {
          item.classList.add('active');
        }
      });
    }
  });

  // ── FAQ Tabs ──
  const faqTabs = document.querySelectorAll('.faq-tab');
  faqTabs.forEach(tab => {
    tab.addEventListener('click', () => {
      faqTabs.forEach(t => t.classList.remove('active'));
      tab.classList.add('active');
    });
  });

  // ── Scanner Page: Drag & Drop (Mock Removed) ──
  // Real integration is handled in scan.html via api.js

  // ── Typing Animation for Code Blocks ──
  const codeBlocks = document.querySelectorAll('.code-block');
  codeBlocks.forEach(block => {
    const codeObserver = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          block.style.opacity = '0';
          block.style.transition = 'opacity 0.5s ease';
          setTimeout(() => {
            block.style.opacity = '1';
          }, 200);
          codeObserver.unobserve(entry.target);
        }
      });
    }, { threshold: 0.3 });

    codeObserver.observe(block);
  });

  // ── Entity Tags Stagger Animation ──
  const entityTags = document.querySelectorAll('.entity-tag');
  if (entityTags.length > 0) {
    const tagObserver = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          const tags = entry.target.querySelectorAll('.entity-tag');
          tags.forEach((tag, i) => {
            setTimeout(() => {
              tag.style.opacity = '1';
              tag.style.transform = 'translateY(0)';
            }, i * 150);
          });
          tagObserver.unobserve(entry.target);
        }
      });
    }, { threshold: 0.5 });

    const tagContainers = document.querySelectorAll('.entity-tags');
    tagContainers.forEach(container => tagObserver.observe(container));
  }

  // ── Table Row Stagger Animation ──
  const tableRows = document.querySelectorAll('.detection-table tbody tr');
  if (tableRows.length > 0) {
    const tableObserver = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          const rows = entry.target.querySelectorAll('tbody tr');
          rows.forEach((row, i) => {
            row.style.opacity = '0';
            row.style.transform = 'translateX(-20px)';
            row.style.transition = `all 0.4s ease ${i * 0.1}s`;
            setTimeout(() => {
              row.style.opacity = '1';
              row.style.transform = 'translateX(0)';
            }, 100);
          });
          tableObserver.unobserve(entry.target);
        }
      });
    }, { threshold: 0.2 });

    const tables = document.querySelectorAll('.detection-showcase');
    tables.forEach(table => tableObserver.observe(table));
  }

  // ── Particle Background Effect ──
  createParticles();
});

function createParticles() {
  const canvas = document.createElement('canvas');
  canvas.id = 'particles';
  canvas.style.cssText = 'position:fixed;top:0;left:0;width:100%;height:100%;pointer-events:none;z-index:0;opacity:0.4;';
  document.body.prepend(canvas);

  const ctx = canvas.getContext('2d');
  let particles = [];
  let animationFrameId;

  function resize() {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
  }

  resize();
  window.addEventListener('resize', resize);

  class Particle {
    constructor() {
      this.reset();
    }

    reset() {
      this.x = Math.random() * canvas.width;
      this.y = Math.random() * canvas.height;
      this.size = Math.random() * 1.5 + 0.5;
      this.speedX = (Math.random() - 0.5) * 0.3;
      this.speedY = (Math.random() - 0.5) * 0.3;
      this.opacity = Math.random() * 0.5 + 0.1;
    }

    update() {
      this.x += this.speedX;
      this.y += this.speedY;

      if (this.x < 0 || this.x > canvas.width) this.speedX *= -1;
      if (this.y < 0 || this.y > canvas.height) this.speedY *= -1;
    }

    draw() {
      ctx.beginPath();
      ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
      ctx.fillStyle = `rgba(59, 130, 246, ${this.opacity})`;
      ctx.fill();
    }
  }

  // Create particles
  const numParticles = Math.min(50, Math.floor(window.innerWidth / 30));
  for (let i = 0; i < numParticles; i++) {
    particles.push(new Particle());
  }

  function animate() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    particles.forEach(p => {
      p.update();
      p.draw();
    });

    // Draw connections
    for (let i = 0; i < particles.length; i++) {
      for (let j = i + 1; j < particles.length; j++) {
        const dx = particles[i].x - particles[j].x;
        const dy = particles[i].y - particles[j].y;
        const dist = Math.sqrt(dx * dx + dy * dy);

        if (dist < 150) {
          ctx.beginPath();
          ctx.moveTo(particles[i].x, particles[i].y);
          ctx.lineTo(particles[j].x, particles[j].y);
          ctx.strokeStyle = `rgba(59, 130, 246, ${0.05 * (1 - dist / 150)})`;
          ctx.lineWidth = 0.5;
          ctx.stroke();
        }
      }
    }

    animationFrameId = requestAnimationFrame(animate);
  }

  animate();
}
