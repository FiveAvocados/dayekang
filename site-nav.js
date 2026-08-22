(() => {
  const header = document.querySelector('header');
  if (!header) return;

  let previousY = Math.max(window.scrollY, 0);
  let scheduled = false;

  const showHeader = () => header.classList.remove('nav-hidden');
  const hideHeader = () => {
    const navigation = header.querySelector('nav');
    if (!navigation?.classList.contains('open')) header.classList.add('nav-hidden');
  };

  const updateHeader = () => {
    const currentY = Math.max(window.scrollY, 0);

    if (currentY <= 40 || currentY < previousY) {
      showHeader();
    } else if (currentY > previousY) {
      hideHeader();
    }

    previousY = currentY;
    scheduled = false;
  };

  window.addEventListener('scroll', () => {
    if (scheduled) return;
    scheduled = true;
    window.requestAnimationFrame(updateHeader);
  }, { passive: true });

  window.addEventListener('pointermove', event => {
    if (event.pointerType === 'mouse' && event.clientY <= 24) showHeader();
  }, { passive: true });

  header.addEventListener('mouseenter', showHeader);
  header.addEventListener('focusin', showHeader);
  header.querySelector('.nav-toggle')?.addEventListener('click', showHeader);
})();
