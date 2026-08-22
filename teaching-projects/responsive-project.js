(() => {
  const makeSvgResponsive = (svg) => {
    const width = Number.parseFloat(svg.getAttribute("width"));
    const height = Number.parseFloat(svg.getAttribute("height"));

    if (!svg.hasAttribute("viewBox") && width > 0 && height > 0) {
      svg.setAttribute("viewBox", `0 0 ${width} ${height}`);
    }

    if (svg.hasAttribute("viewBox")) {
      svg.setAttribute("preserveAspectRatio", "xMidYMid meet");
      svg.style.maxWidth = "100%";
      svg.style.height = "auto";
    }
  };

  const updateSvgs = (root) => {
    if (root instanceof SVGElement) {
      makeSvgResponsive(root.ownerSVGElement || root);
    }
    root.querySelectorAll?.("svg").forEach(makeSvgResponsive);
  };

  const initialize = () => {
    updateSvgs(document);

    new MutationObserver((mutations) => {
      mutations.forEach((mutation) => {
        mutation.addedNodes.forEach((node) => {
          if (node instanceof Element) updateSvgs(node);
        });
      });
    }).observe(document.body, {
      childList: true,
      subtree: true,
      attributes: true,
      attributeFilter: ["width", "height"]
    });
  };

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initialize, { once: true });
  } else {
    initialize();
  }
})();
