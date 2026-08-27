document.querySelectorAll('[data-carousel]').forEach((carousel) => {
  const track = carousel.querySelector('[data-carousel-track]');
  const slides = Array.from(track?.children || []);
  const previous = carousel.querySelector('[data-carousel-prev]');
  const next = carousel.querySelector('[data-carousel-next]');
  const status = carousel.querySelector('[data-carousel-status]');

  if (!track || !previous || !next || !status || slides.length === 0) return;

  previous.setAttribute('aria-controls', track.id);
  next.setAttribute('aria-controls', track.id);

  const currentIndex = () => {
    const slideWidth = Math.max(track.clientWidth, 1);
    return Math.min(slides.length - 1, Math.max(0, Math.round(track.scrollLeft / slideWidth)));
  };

  const update = () => {
    const index = currentIndex();
    status.textContent = `${index + 1} / ${slides.length}`;
    previous.disabled = index === 0;
    next.disabled = index === slides.length - 1;
  };

  const move = (direction) => {
    const index = Math.min(slides.length - 1, Math.max(0, currentIndex() + direction));
    track.scrollTo({ left: index * track.clientWidth, behavior: 'smooth' });
  };

  previous.addEventListener('click', () => move(-1));
  next.addEventListener('click', () => move(1));

  let frame;
  track.addEventListener('scroll', () => {
    cancelAnimationFrame(frame);
    frame = requestAnimationFrame(update);
  }, { passive: true });

  if ('ResizeObserver' in window) new ResizeObserver(update).observe(track);
  update();
});
