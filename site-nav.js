(() => {
  const header = document.querySelector('header');
  if (!header) return;

  const videoHero = document.body.classList.contains('video-hero-page')
    ? document.querySelector('.ux-video-hero, .artwork-video-hero')
    : null;

  let previousY = Math.max(window.scrollY, 0);
  let scheduled = false;

  const showHeader = () => header.classList.remove('nav-hidden');
  const hideHeader = () => {
    const navigation = header.querySelector('nav');
    if (!navigation?.classList.contains('open')) header.classList.add('nav-hidden');
  };

  const updateVideoHeader = () => {
    if (!videoHero) return;
    const heroBottom = videoHero.getBoundingClientRect().bottom;
    header.classList.toggle('video-header-solid', heroBottom <= header.offsetHeight);
  };

  const updateHeader = () => {
    const currentY = Math.max(window.scrollY, 0);

    if (videoHero) {
      showHeader();
      updateVideoHeader();
    } else if (currentY <= 40 || currentY < previousY) {
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

  if (videoHero) {
    updateVideoHeader();
    window.addEventListener('resize', updateVideoHeader, { passive: true });
  }

  window.addEventListener('pointermove', event => {
    if (event.pointerType === 'mouse' && event.clientY <= 24) showHeader();
  }, { passive: true });

  header.addEventListener('mouseenter', showHeader);
  header.addEventListener('focusin', showHeader);
  header.querySelector('.nav-toggle')?.addEventListener('click', showHeader);
})();
