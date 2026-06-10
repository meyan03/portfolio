// Smooth reveal on scroll
const observer = new IntersectionObserver((entries) => {
  entries.forEach(e => {
    if (e.isIntersecting) {
      e.target.classList.add('visible');
      observer.unobserve(e.target);
    }
  });
}, { rootMargin: "0px 0px -10% 0px", threshold: 0.1 });

window.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('section, .card').forEach(el => {
    el.classList.add('reveal');
    observer.observe(el);
  });
});
