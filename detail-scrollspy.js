(() => {
  const sections = [
    document.getElementById('intro'),
    ...document.querySelectorAll('.dsec'),
  ].filter(Boolean);
  const links = [...document.querySelectorAll('.side-nav a')];

  if (!sections.length || !links.length) return;

  const update = () => {
    let current = 0;
    sections.forEach((section, index) => {
      if (section.getBoundingClientRect().top < 160) current = index;
    });
    links.forEach((link, index) => link.classList.toggle('on', index === current));
  };

  document.addEventListener('scroll', update, { passive: true });
  window.addEventListener('resize', update);
  update();
})();
