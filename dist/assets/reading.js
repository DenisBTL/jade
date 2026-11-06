/* Navigation de lecture adaptée des conventions Pepper / Mon Chai. */
(() => {
  const scenes = [...document.querySelectorAll('[data-reading-scene]')];
  const fill = document.querySelector('#readbar-fill');
  const sceneLinks = [...document.querySelectorAll('.scene-nav a')];
  if (!scenes.length || !fill) return;
  const reducedMotion = matchMedia('(prefers-reduced-motion: reduce)');
  document.documentElement.classList.add('reading-ready');
  let readingFrame = null;
  let glideFrame = null;
  let departureTimer = null;

  function updateReading() {
    readingFrame = null;
    const y = Math.max(0, window.scrollY);
    const total = Math.max(0, document.documentElement.scrollHeight - innerHeight);
    const progress = total > 0 ? Math.min(1, y / total) : 0;
    fill.style.transform = `scaleX(${progress})`;
    let current = scenes[0];
    for (const scene of scenes) {
      if (scene.getBoundingClientRect().top <= innerHeight * 0.5) current = scene;
    }
    if (y >= total - 2) current = scenes.at(-1);
    for (const link of sceneLinks) {
      if (link.hash === '#' + current.id) link.setAttribute('aria-current', 'location');
      else link.removeAttribute('aria-current');
    }
  }
  function queueReading() {
    if (readingFrame === null) readingFrame = requestAnimationFrame(updateReading);
  }
  window.addEventListener('scroll', queueReading, { passive: true });
  window.addEventListener('resize', queueReading, { passive: true });
  window.addEventListener('pageshow', queueReading);
  new ResizeObserver(queueReading).observe(document.body);
  document.fonts?.ready.then(queueReading);
  queueReading();

  function cancelGlide() {
    if (glideFrame !== null) cancelAnimationFrame(glideFrame);
    if (departureTimer !== null) clearTimeout(departureTimer);
    glideFrame = null;
    departureTimer = null;
  }
  for (const type of ['wheel', 'touchstart', 'pointerdown', 'keydown']) {
    window.addEventListener(type, cancelGlide, { passive: true });
  }
  reducedMotion.addEventListener('change', cancelGlide);

  function arrive(target) {
    const url = new URL(location.href);
    url.hash = target.id;
    history.replaceState(null, '', url);
    if (!target.hasAttribute('tabindex')) {
      target.setAttribute('tabindex', '-1');
      target.addEventListener('blur', () => target.removeAttribute('tabindex'), { once: true });
    }
    target.focus({ preventScroll: true });
    queueReading();
  }
  function glide(target) {
    departureTimer = null;
    const start = Math.max(0, scrollY);
    const maximum = Math.max(0, document.documentElement.scrollHeight - innerHeight);
    const end = Math.max(0, Math.min(maximum, target.getBoundingClientRect().top + start - 24));
    const distance = end - start;
    if (reducedMotion.matches || Math.abs(distance) < 2) {
      window.scrollTo({ top: end, behavior: 'instant' });
      arrive(target);
      return;
    }
    const duration = Math.min(1100, Math.max(650, Math.abs(distance) * 0.5));
    let started;
    function step(now) {
      started ??= now;
      const progress = Math.min(1, (now - started) / duration);
      const eased = progress < 0.5 ? 4 * progress ** 3 : 1 - (-2 * progress + 2) ** 3 / 2;
      window.scrollTo({ top: start + distance * eased, behavior: 'instant' });
      if (progress < 1) glideFrame = requestAnimationFrame(step);
      else { glideFrame = null; arrive(target); }
    }
    glideFrame = requestAnimationFrame(step);
  }
  document.addEventListener('click', event => {
    const link = event.target.closest('.scene-next, .scene-nav a');
    if (!link || event.defaultPrevented || event.button !== 0 || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
    const target = document.getElementById(link.hash.slice(1));
    if (!target) return;
    event.preventDefault();
    cancelGlide();
    if (link.hasAttribute('data-water-cue') && !reducedMotion.matches && document.querySelector('.home-water-canvas.is-ready')) {
      const hero = document.querySelector('.home-hero');
      const rect = hero.getBoundingClientRect();
      const ring = link.querySelector('.scene-next-ring').getBoundingClientRect();
      hero.dispatchEvent(new CustomEvent('jade:water-ripple', { detail: {
        x: ring.left + ring.width / 2 - rect.left,
        y: ring.top + ring.height / 2 - rect.top,
      } }));
      departureTimer = setTimeout(() => glide(target), 420);
    } else glide(target);
  });
})();
