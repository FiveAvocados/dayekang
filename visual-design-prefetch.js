(() => {
  const connection = navigator.connection || navigator.mozConnection || navigator.webkitConnection;
  if (connection?.saveData || /(^|-)2g$/.test(connection?.effectiveType || "")) return;

  const version = "?v=20260825-gallery-fast";
  const assets = [
    "assets/optimized/video/bird4.mp4",
    ...Array.from({ length: 30 }, (_, index) => {
      const number = String(index + 1).padStart(2, "0");
      return `assets/optimized/gallery/art_${number}-1200.webp${version}`;
    })
  ];

  let started = false;
  const warmCache = async () => {
    if (started) return;
    started = true;

    let next = 0;
    const worker = async () => {
      while (next < assets.length) {
        const asset = assets[next++];
        try {
          const response = await fetch(asset, {
            cache: "force-cache",
            credentials: "same-origin",
            priority: "low"
          });
          if (response.ok) await response.blob();
        } catch (_) {
          // Prefetching is an optional speed-up. Normal navigation still works.
        }
      }
    };

    await Promise.all([worker(), worker(), worker()]);
  };

  const schedule = () => {
    if ("requestIdleCallback" in window) {
      window.requestIdleCallback(warmCache, { timeout: 3500 });
    } else {
      window.setTimeout(warmCache, 1500);
    }
  };

  const visualDesignLink = document.querySelector('a[href^="visual-design.html"]');
  visualDesignLink?.addEventListener("pointerenter", warmCache, { once: true, passive: true });
  visualDesignLink?.addEventListener("focus", warmCache, { once: true });
  visualDesignLink?.addEventListener("touchstart", warmCache, { once: true, passive: true });

  if (document.readyState === "complete") schedule();
  else window.addEventListener("load", schedule, { once: true });
})();
