
// Smooth reveal on scroll
const revealables = new Set();
const observer = new IntersectionObserver((entries)=>{
  entries.forEach(e=>{
    if(e.isIntersecting){
      e.target.classList.add('visible');
      observer.unobserve(e.target);
      revealables.delete(e.target);
    }
  })
},{ rootMargin: "0px 0px -10% 0px", threshold: 0.1 });

function markReveal(el){
  if(!el.classList.contains('reveal')) el.classList.add('reveal');
  revealables.add(el);
  observer.observe(el);
}

window.addEventListener('DOMContentLoaded', ()=>{
  // auto-attach reveal to sections, articles, cards, table rows, list items
  document.querySelectorAll('section, article, .card, tbody tr, li, .hero').forEach(markReveal);

  // wrap main content to container if not already
  if(!document.querySelector('.container')){
    const main = document.querySelector('main') || document.body;
    const wrapper = document.createElement('div');
    wrapper.className = 'container';
    while(main.firstChild){
      wrapper.appendChild(main.firstChild);
    }
    main.appendChild(wrapper);
  }

  // if no header exists, create a simple sticky header without changing existing content
  if(!document.querySelector('header.site')){
    const header = document.createElement('header');
    header.className = 'site';
    header.innerHTML = `
      <div class="container nav">
        <a class="brand" href="index.html"><span class="dot"></span><span>Portfolio</span></a>
        <nav class="links" aria-label="Navigation"></nav>
      </div>
    `;
    document.body.prepend(header);

    // Build quick links from any on-page anchors
    const linksNav = header.querySelector('.links');
    const seen = new Set();
    document.querySelectorAll('a[href^="#"]').forEach(a=>{
      const id = a.getAttribute('href');
      if(id && !seen.has(id)){
        const clone = a.cloneNode(true);
        clone.classList.remove('btn');
        linksNav.appendChild(clone);
        seen.add(id);
      }
    });
  }
});
