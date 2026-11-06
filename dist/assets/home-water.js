/* Reflets Canvas 2D : aucun besoin d'accélération graphique ou de WebGL. */
(() => {
  const hero = document.querySelector('.home-hero');
  const image = hero?.querySelector('.home-landscape');
  const canvas = hero?.querySelector('.home-water-canvas');
  const toggle = hero?.querySelector('.water-toggle');
  const splash = hero?.querySelector('.water-splash');
  if (!image || !canvas || !toggle || !splash) return;
  const reducedMotion = matchMedia('(prefers-reduced-motion: reduce)');
  let context;
  let initialized = false;
  let failed = false;
  let paused = false;
  let visible = false;
  let frame = 0;
  let previous = 0;
  let elapsed = 0;
  let hits = [];
  let width = 0;
  let height = 0;
  let scale = 1;
  let offsetX = 0;
  let offsetY = 0;
  let waterTop = 0;
  let waterPath;
  let ratio = 1;
  let sourcePixels;
  let waveCanvas;
  let waveContext;
  let wavePixels;
  let startRow = 0;
  let columnShores;
  let foliageBounds;
  let foliageCanvas;
  let foliageContext;
  let foliagePixels;
  let foliageWeights;
  let foliageAlpha;
  let foliageStartX;
  let foliageStartY;
  let visibleLeaves = [];
  const canopy = [[0.49,0.752],[0.52,0.742],[0.54,0.690],[0.575,0.670],
    [0.61,0.672],[0.645,0.700],[0.67,0.680],[0.70,0.660],[0.74,0.634],
    [0.77,0.642],[0.80,0.637],[0.83,0.665],[0.85,0.668],[0.88,0.654],
    [0.91,0.640],[0.93,0.616],[0.95,0.590],[0.98,0.550],[1,0.538]];
  const treeBases = [[1,0.741],[0.95,0.745],[0.90,0.737],[0.86,0.740],
    [0.80,0.743],[0.75,0.732],[0.70,0.740],[0.65,0.735],[0.60,0.750],
    [0.55,0.756],[0.49,0.766]];
  const leaves = Array.from({ length: 13 }, (_, i) => ({
    x: 0.54 + i * 0.036,
    phase: (0.12 + i * 0.271) % 1,
    duration: 9 + (i % 4) * 1.1,
    size: 6 + (i % 3),
    color: ['#756383', '#6c7890', '#a38b5d', '#8a7299'][i % 4],
  }));

  function canopyAt(x) {
    for (let i = 1; i < canopy.length; i++) {
      if (x <= canopy[i][0]) {
        const a = canopy[i - 1], b = canopy[i];
        const t = Math.max(0, Math.min(1, (x - a[0]) / (b[0] - a[0])));
        return a[1] + (b[1] - a[1]) * t;
      }
    }
    return canopy[canopy.length - 1][1];
  }

  function renderFoliage() {
    const pixels = foliagePixels.data;
    const original = sourcePixels.data;
    const pixelWidth = canvas.width;
    const wind = Math.sin(elapsed * 0.38) * 3.2;
    for (let row = 0; row < foliageCanvas.height; row++) {
      const y = (foliageStartY + row + 0.5) / ratio;
      for (let col = 0; col < foliageCanvas.width; col++) {
        const cell = row * foliageCanvas.width + col;
        const index = cell * 4;
        const alpha = foliageAlpha[cell];
        pixels[index + 3] = alpha;
        if (alpha === 0) continue;
        const x = (foliageStartX + col + 0.5) / ratio;
        const spring = foliageWeights[cell];
        const dx = (Math.sin(elapsed * 0.92 + x * 0.023) * 2.8
          + Math.sin(elapsed * 0.47 + x * 0.007) * 2.2 + wind) * spring;
        const dy = Math.sin(elapsed * 0.8 + x * 0.015) * 1.15 * spring;
        const sx = Math.max(0, Math.min(pixelWidth - 1.001, (x - dx) * ratio));
        const sy = Math.max(0, Math.min(canvas.height - 1.001, (y - dy) * ratio));
        const ix = Math.floor(sx), iy = Math.floor(sy);
        const fx = sx - ix, fy = sy - iy;
        const upper = (iy * pixelWidth + ix) * 4;
        const lower = upper + pixelWidth * 4;
        for (let channel = 0; channel < 3; channel++) {
          const a = original[upper + channel] * (1 - fx) + original[upper + 4 + channel] * fx;
          const b = original[lower + channel] * (1 - fx) + original[lower + 4 + channel] * fx;
          pixels[index + channel] = a * (1 - fy) + b * fy;
        }
      }
    }
    foliageContext.putImageData(foliagePixels, 0, 0);
    context.drawImage(foliageCanvas, foliageStartX / ratio, foliageStartY / ratio,
      foliageCanvas.width / ratio, foliageCanvas.height / ratio);
  }

  function renderLeaves() {
    for (let i = 0; i < visibleLeaves.length; i++) {
      const leaf = visibleLeaves[i];
      const progress = (elapsed / leaf.duration + leaf.phase) % 1;
      const x = (leaf.x + progress * 0.038 + Math.sin(elapsed * 0.75 + i * 2.1) * 0.009) * image.naturalWidth * scale + offsetX;
      const y = (canopyAt(leaf.x) + 0.008 + progress * 0.105) * image.naturalHeight * scale + offsetY;
      if (x < -10 || x > width + 10 || y < 0 || y > height - 65) continue;
      const opacity = Math.min(1, progress / 0.12, (1 - progress) / 0.25) * 0.82;
      const size = Math.max(5, Math.min(9, leaf.size * scale));
      context.save();
      context.globalAlpha = opacity;
      context.translate(x, y);
      context.rotate(Math.sin(elapsed * 1.3 + i) * 0.9 + progress * 3.5);
      context.scale(0.45 + Math.abs(Math.cos(elapsed * 1.1 + i)) * 0.55, 1);
      context.beginPath();
      context.moveTo(-size, 0);
      context.bezierCurveTo(-size * 0.2, -size * 0.8, size * 0.9, -size * 0.5, size, 0);
      context.bezierCurveTo(size * 0.1, size * 0.75, -size * 0.8, size * 0.45, -size, 0);
      context.fillStyle = leaf.color;
      context.fill();
      context.beginPath();
      context.moveTo(-size * 0.8, 0);
      context.lineTo(size * 0.7, 0);
      context.strokeStyle = '#d3bb86';
      context.lineWidth = 0.5;
      context.stroke();
      context.restore();
    }
  }

  function shoreAt(x) {
    const smooth = (a, b, value) => {
      const t = Math.max(0, Math.min(1, (value - a) / (b - a)));
      return t * t * (3 - 2 * t);
    };
    return 0.86 - 0.10 * smooth(0, 0.58, x) + 0.025 * smooth(0.65, 1, x);
  }

  function stop() {
    cancelAnimationFrame(frame);
    frame = 0;
    previous = 0;
  }

  function unavailable() {
    failed = true;
    stop();
    canvas.classList.remove('is-ready');
    toggle.hidden = true;
    splash.hidden = true;
  }

  function renderPulse() {
    const pixelWidth = canvas.width;
    const pixels = wavePixels.data;
    const original = sourcePixels.data;
    for (let row = 0; row < waveCanvas.height; row++) {
      const y = (startRow + row + 0.5) / ratio;
      const flow = Math.sin(y * 0.13 - elapsed * 0.9 + Math.sin(elapsed * 0.27)) * 7;
      const swell = Math.sin(y * 0.19 + elapsed * 0.65) * 2.4;
      for (let col = 0; col < pixelWidth; col++) {
        const index = (row * pixelWidth + col) * 4;
        const x = (col + 0.5) / ratio;
        const shore = columnShores[col];
        const depth = Math.max(0, Math.min(1, (y - shore) / Math.max(1, height - shore)));
        if (depth <= 0) { pixels[index + 3] = 0; continue; }
        const envelope = Math.min(1, depth * 4);
        let dx = flow * depth;
        let dy = swell * depth;
        let light = 0;
        for (const hit of hits) {
          const age = elapsed - hit.at;
          const horizontal = x - hit.x;
          const vertical = (y - hit.y) * 2.5;
          const distance = Math.hypot(horizontal, vertical);
          const front = Math.exp(-Math.pow((distance - age * 210) / 190, 2));
          const power = Math.sin(distance * 0.065 - age * 10) * 85 * Math.exp(-age * 0.85) * front * envelope;
          dx += horizontal / Math.max(1, distance) * power;
          dy += vertical / Math.max(1, distance) * power * 0.45;
          light += power * 0.12 * depth;
        }
        const sx = Math.max(0, Math.min(pixelWidth - 1.001, (x + Math.max(-100, Math.min(100, dx))) * ratio));
        const sy = Math.max(0, Math.min(canvas.height - 1.001, (y + Math.max(-42, Math.min(42, dy))) * ratio));
        const ix = Math.floor(sx), iy = Math.floor(sy);
        const fx = sx - ix, fy = sy - iy;
        const a = (iy * pixelWidth + ix) * 4;
        const b = a + pixelWidth * 4;
        // Interpolation des reflets pixel par pixel : aucune mosaïque de tuiles.
        for (let channel = 0; channel < 3; channel++) {
          const upper = original[a + channel] * (1 - fx) + original[a + 4 + channel] * fx;
          const lower = original[b + channel] * (1 - fx) + original[b + 4 + channel] * fx;
          pixels[index + channel] = upper * (1 - fy) + lower * fy + light;
        }
        pixels[index + 3] = 255;
      }
    }
    waveContext.putImageData(wavePixels, 0, 0);
    context.drawImage(waveCanvas, 0, startRow / ratio, canvas.width / ratio, waveCanvas.height / ratio);
  }

  function render() {
    context.clearRect(0, 0, width, height);
    renderFoliage();
    context.save();
    context.clip(waterPath);
    hits = hits.filter(hit => elapsed - hit.at < 5);
    if (hits.length) {
      renderPulse();
      context.restore();
      renderLeaves();
      return;
    }
    const rowHeight = 3;
    for (let y = waterTop; y < height; y += rowHeight) {
        const centerY = y + rowHeight / 2;
        const sourceX = (width / 2 - offsetX) / scale;
        const shore = shoreAt(sourceX / image.naturalWidth) * image.naturalHeight * scale + offsetY;
        const depth = Math.max(0, Math.min(1, (centerY - shore) / Math.max(1, height - shore)));
        const dx = Math.sin(y * 0.13 - elapsed * 0.9 + Math.sin(elapsed * 0.27)) * 7 * depth;
        const dy = Math.sin(y * 0.19 + elapsed * 0.65) * 2.4 * depth;
        const sampleX = (dx - offsetX) / scale;
        const sampleY = (y + dy - offsetY) / scale;
        context.drawImage(image, sampleX, sampleY, width / scale, rowHeight / scale, 0, y, width, rowHeight);
    }
    context.restore();
    renderLeaves();
  }

  function resize() {
    const rect = hero.getBoundingClientRect();
    width = rect.width;
    height = rect.height;
    ratio = Math.min(devicePixelRatio || 1, 1.25, 900 / Math.max(1, width));
    canvas.width = Math.max(1, Math.round(width * ratio));
    canvas.height = Math.max(1, Math.round(height * ratio));
    context.setTransform(ratio, 0, 0, ratio, 0, 0);
    context.imageSmoothingEnabled = true;
    scale = Math.max(width / image.naturalWidth, height / image.naturalHeight);
    const mobile = matchMedia('(max-width: 700px)').matches;
    offsetX = (width - image.naturalWidth * scale) * (mobile ? 0.57 : 0.5);
    offsetY = (height - image.naturalHeight * scale) * (mobile ? 1 : 0.5);
    waterPath = new Path2D();
    waterPath.moveTo(0, height);
    waterTop = height;
    for (let x = 0; x <= width + 16; x += 16) {
      const shore = shoreAt((x - offsetX) / scale / image.naturalWidth) + 0.018;
      const y = shore * image.naturalHeight * scale + offsetY;
      waterTop = Math.min(waterTop, y);
      waterPath.lineTo(x, y);
    }
    waterPath.lineTo(width, height);
    waterPath.closePath();
    waterTop = Math.max(0, Math.floor(waterTop));
    const sourceCanvas = document.createElement('canvas');
    sourceCanvas.width = canvas.width;
    sourceCanvas.height = canvas.height;
    const sourceContext = sourceCanvas.getContext('2d', { willReadFrequently: true });
    sourceContext.setTransform(ratio, 0, 0, ratio, 0, 0);
    sourceContext.drawImage(image, offsetX, offsetY, image.naturalWidth * scale, image.naturalHeight * scale);
    sourcePixels = sourceContext.getImageData(0, 0, canvas.width, canvas.height);
    startRow = Math.floor(waterTop * ratio);
    waveCanvas = document.createElement('canvas');
    waveCanvas.width = canvas.width;
    waveCanvas.height = Math.max(1, canvas.height - startRow);
    waveContext = waveCanvas.getContext('2d');
    wavePixels = waveContext.createImageData(waveCanvas.width, waveCanvas.height);
    columnShores = new Float32Array(canvas.width);
    for (let col = 0; col < canvas.width; col++) {
      columnShores[col] = shoreAt(((col + 0.5) / ratio - offsetX) / scale / image.naturalWidth) * image.naturalHeight * scale + offsetY;
    }
    const pointAt = (points, x) => {
      for (let i = 1; i < points.length; i++) {
        if (x <= points[i][0]) {
          const a = points[i - 1], b = points[i];
          const t = Math.max(0, Math.min(1, (x - a[0]) / (b[0] - a[0])));
          return a[1] + (b[1] - a[1]) * t;
        }
      }
      return points[points.length - 1][1];
    };
    const bases = [...treeBases].reverse();
    const points = [...canopy, ...treeBases].map(([x, y]) =>
      [x * image.naturalWidth * scale + offsetX, y * image.naturalHeight * scale + offsetY]);
    foliageBounds = {
      left: Math.max(0, Math.floor(Math.min(...points.map(p => p[0])))),
      right: Math.min(width, Math.ceil(Math.max(...points.map(p => p[0])))),
      top: Math.max(0, Math.floor(Math.min(...points.map(p => p[1])))),
      bottom: Math.min(height, Math.ceil(Math.max(...points.map(p => p[1])))),
    };
    foliageStartX = Math.floor(foliageBounds.left * ratio);
    foliageStartY = Math.floor(foliageBounds.top * ratio);
    foliageCanvas = document.createElement('canvas');
    foliageCanvas.width = Math.max(1, Math.ceil(foliageBounds.right * ratio) - foliageStartX);
    foliageCanvas.height = Math.max(1, Math.ceil(foliageBounds.bottom * ratio) - foliageStartY);
    foliageContext = foliageCanvas.getContext('2d');
    foliagePixels = foliageContext.createImageData(foliageCanvas.width, foliageCanvas.height);
    foliageWeights = new Float32Array(foliageCanvas.width * foliageCanvas.height);
    foliageAlpha = new Uint8Array(foliageWeights.length);
    for (let col = 0; col < foliageCanvas.width; col++) {
      const x = (foliageStartX + col + 0.5) / ratio;
      const u = (x - offsetX) / scale / image.naturalWidth;
      const top = canopyAt(u) * image.naturalHeight * scale + offsetY;
      const bottom = pointAt(bases, u) * image.naturalHeight * scale + offsetY;
      for (let row = 0; row < foliageCanvas.height; row++) {
        const y = (foliageStartY + row + 0.5) / ratio;
        const index = row * foliageCanvas.width + col;
        foliageAlpha[index] = Math.round(Math.max(0, Math.min(1, (y - top) / 3.5, (bottom - y) / 4)) * 255);
        foliageWeights[index] = Math.max(0, Math.min(1, (bottom - y) / Math.max(1, bottom - top)));
      }
    }
    const candidates = leaves.filter(leaf => {
      const x = leaf.x * image.naturalWidth * scale + offsetX;
      return x > 5 && x < width - 5;
    });
    const count = Math.min(candidates.length, width <= 700 ? 5 : 9);
    visibleLeaves = Array.from({ length: count }, (_, i) => candidates[Math.floor(i * candidates.length / count)]);
    hits = [];
    render();
  }

  function initialize() {
    if (initialized || failed || reducedMotion.matches || !image.complete || !image.naturalWidth) return;
    try {
      context = canvas.getContext('2d', { alpha: true });
      if (!context) { unavailable(); return; }
      initialized = true;
      new ResizeObserver(resize).observe(hero);
      resize();
    } catch { unavailable(); }
  }

  function tick(now) {
    frame = requestAnimationFrame(tick);
    if (previous && now - previous < 1000 / 24) return;
    if (previous) elapsed += Math.max(0, (now - previous) / 1000);
    previous = now;
    render();
  }

  function sync() {
    initialize();
    const enabled = initialized && !failed && !reducedMotion.matches;
    toggle.hidden = !enabled;
    splash.hidden = !enabled;
    canvas.classList.toggle('is-ready', enabled);
    toggle.setAttribute('aria-pressed', String(paused));
    toggle.setAttribute('aria-label', paused ? 'Animer le paysage' : 'Mettre les animations du paysage en pause');
    toggle.querySelector('.water-toggle-text').textContent = paused ? 'Reprendre' : 'Pause';
    toggle.querySelector('.water-toggle-icon').textContent = paused ? '▷' : 'Ⅱ';
    if (enabled && !paused && visible && !document.hidden) {
      if (!frame) frame = requestAnimationFrame(tick);
    } else stop();
  }

  splash.addEventListener('click', event => {
    if (!initialized || failed || reducedMotion.matches) return;
    const rect = hero.getBoundingClientRect();
    // Entrée / Espace déclenchent l'onde au centre du lac.
    const x = event.detail === 0 ? width * 0.5 : event.clientX - rect.left;
    const y = event.detail === 0 ? height * 0.91 : event.clientY - rect.top;
    hits.push({ x, y, at: elapsed });
    hits = hits.slice(-4);
    paused = false;
    render();
    sync();
  });
  toggle.addEventListener('click', () => { paused = !paused; sync(); });
  reducedMotion.addEventListener('change', sync);
  document.addEventListener('visibilitychange', sync);
  canvas.addEventListener('contextlost', unavailable);
  new IntersectionObserver(entries => { visible = entries[0].isIntersecting; sync(); }).observe(hero);
  image.addEventListener('load', sync, { once: true });
  sync();
})();
