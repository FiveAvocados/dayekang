(function () {
  const slugify = (value) => (value || "project")
    .toLowerCase()
    .normalize("NFKD")
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/^-+|-+$/g, "") || "project";

  const configuredGroupFor = (title) => (window.VISUAL_PROJECT_GROUPS || [])
    .find((group) => (group.titles || []).includes(title));

  const projectIdFor = (art) => {
    const title = art.dataset.title || "Project";
    const group = configuredGroupFor(title);
    return group ? group.id : slugify(title);
  };

  const absoluteAsset = (path) => new URL(path, window.location.href).href;
  const requestedId = new URLSearchParams(window.location.search).get("project");
  const projectShell = document.querySelector(".visual-project-shell");
  const mediaRoot = document.getElementById("visual-project-media");
  const infoRoot = document.getElementById("visual-project-info");
  const titleNode = document.getElementById("visual-project-title");
  const metaNode = document.getElementById("visual-project-meta");
  const descriptionNode = document.getElementById("visual-project-description");

  const showError = () => {
    titleNode.textContent = "Project not found";
    descriptionNode.innerHTML = '<p><a href="visual-design.html">Return to Visual Design</a></p>';
    infoRoot.classList.remove("is-empty");
  };

  fetch("visual-design.html?v=20261027-qinqin-roles")
    .then((response) => {
      if (!response.ok) throw new Error("Artwork page could not be loaded.");
      return response.text();
    })
    .then((markup) => {
      const documentCopy = new DOMParser().parseFromString(markup, "text/html");
      const arts = [...documentCopy.querySelectorAll(".gallery .art")];
      const order = [];
      const projects = new Map();

      arts.forEach((art) => {
        const id = projectIdFor(art);
        if (!projects.has(id)) {
          projects.set(id, []);
          order.push(id);
        }
        projects.get(id).push(art);
      });

      const currentId = projects.has(requestedId) ? requestedId : order[0];
      const items = projects.get(currentId);
      if (!items || !items.length) return showError();

      const configured = (window.VISUAL_PROJECT_CONTENT || {})[currentId] || {};
      const group = (window.VISUAL_PROJECT_GROUPS || []).find((item) => item.id === currentId) || {};
      const title = configured.title || group.title || items[0].dataset.title || "Visual Design Project";
      titleNode.textContent = title;
      document.title = `${title} — Daye Kang`;

      const relatedTitles = configured.mediaFromTitles || [];
      const relatedItems = arts.filter((art) => relatedTitles.includes(art.dataset.title || ""));
      const mediaItems = configured.replaceMedia ? [] : [...items, ...relatedItems];

      const configureVideo = (video) => {
        video.controls = true;
        video.autoplay = true;
        video.defaultMuted = true;
        video.muted = true;
        video.loop = true;
        video.playsInline = true;
        video.preload = "metadata";
        return video;
      };

      const createMedia = ({ src, alt, type, poster }) => {
        if (!src) return null;
        if (type === "video") {
          const video = document.createElement("video");
          video.src = absoluteAsset(src);
          if (poster) video.poster = absoluteAsset(poster);
          return configureVideo(video);
        }
        const image = document.createElement("img");
        image.src = absoluteAsset(src);
        image.alt = alt || title;
        image.decoding = "async";
        image.loading = "lazy";
        return image;
      };

      const mediaFragment = document.createDocumentFragment();

      const appendAdditionalMedia = () => {
        (configured.additionalMedia || []).forEach((item) => {
          const media = createMedia(item);
          if (media) mediaFragment.appendChild(media);
        });
      };

      if (configured.additionalMediaPosition === "before") appendAdditionalMedia();

      mediaItems.forEach((item) => {
        const source = item.querySelector("img, video");
        if (!source) return;
        const sourcePath = source.dataset.fullSrc || source.getAttribute("src") || source.dataset.src;
        if (!sourcePath) return;
        let media;
        if (source.tagName === "VIDEO") {
          media = configureVideo(document.createElement("video"));
          media.src = absoluteAsset(sourcePath);
          const sourcePoster = source.getAttribute("poster");
          if (sourcePoster) media.poster = absoluteAsset(sourcePoster);
        } else {
          media = document.createElement("img");
          media.src = absoluteAsset(sourcePath);
          media.alt = source.getAttribute("alt") || title;
          media.decoding = "async";
        }
        mediaFragment.appendChild(media);
      });

      if (configured.additionalMediaPosition !== "before") appendAdditionalMedia();

      let mediaCount = mediaFragment.childElementCount;
      if (configured.mediaLayout === "horizontal-strip") {
        const strip = document.createElement("div");
        strip.className = "visual-project-strip";
        strip.setAttribute("role", "region");
        strip.setAttribute("aria-label", `${title} animation frames`);
        strip.appendChild(mediaFragment);
        mediaRoot.appendChild(strip);
        projectShell.classList.add("has-horizontal-media");
      } else {
        mediaRoot.appendChild(mediaFragment);
      }

      if ((configured.mediaSections || []).length) {
        document.querySelectorAll(".visual-project-nav").forEach((nav) => {
          nav.hidden = true;
        });
      }

      (configured.mediaSections || []).forEach((section, sectionIndex) => {
        const sectionRoot = document.createElement("section");
        sectionRoot.className = "visual-project-storyboard";
        const heading = document.createElement("h2");
        heading.id = `${currentId}-media-section-${sectionIndex + 1}`;
        heading.textContent = section.title || `Storyboard ${sectionIndex + 1}`;
        sectionRoot.setAttribute("aria-labelledby", heading.id);

        const strip = document.createElement("div");
        strip.className = "visual-project-strip";
        strip.id = `${currentId}-media-strip-${sectionIndex + 1}`;
        strip.setAttribute("role", "region");
        strip.setAttribute("aria-label", section.ariaLabel || heading.textContent);
        strip.tabIndex = 0;
        (section.media || []).forEach((item) => {
          const media = createMedia(item);
          if (media) strip.appendChild(media);
        });
        if (!strip.childElementCount) return;

        const carousel = document.createElement("div");
        carousel.className = "visual-project-carousel";
        const previousButton = document.createElement("button");
        previousButton.className = "visual-project-carousel-button is-previous";
        previousButton.type = "button";
        previousButton.setAttribute("aria-label", `Previous ${heading.textContent} frame`);
        previousButton.setAttribute("aria-controls", strip.id);
        previousButton.innerHTML = "&#8249;";
        const nextButton = document.createElement("button");
        nextButton.className = "visual-project-carousel-button is-next";
        nextButton.type = "button";
        nextButton.setAttribute("aria-label", `Next ${heading.textContent} frame`);
        nextButton.setAttribute("aria-controls", strip.id);
        nextButton.innerHTML = "&#8250;";

        const moveCarousel = (direction) => {
          const firstFrame = strip.firstElementChild;
          const gap = parseFloat(getComputedStyle(strip).columnGap) || 0;
          const step = (firstFrame?.getBoundingClientRect().width || strip.clientWidth) + gap;
          const maxScroll = strip.scrollWidth - strip.clientWidth;
          let target = strip.scrollLeft + direction * step;
          if (direction < 0 && strip.scrollLeft <= 2) target = maxScroll;
          if (direction > 0 && strip.scrollLeft >= maxScroll - 2) target = 0;
          strip.scrollTo({ left: target, behavior: "smooth" });
        };
        previousButton.addEventListener("click", () => moveCarousel(-1));
        nextButton.addEventListener("click", () => moveCarousel(1));
        strip.addEventListener("keydown", (event) => {
          if (event.key !== "ArrowLeft" && event.key !== "ArrowRight") return;
          event.preventDefault();
          event.stopPropagation();
          moveCarousel(event.key === "ArrowLeft" ? -1 : 1);
        });
        carousel.append(previousButton, strip, nextButton);

        mediaCount += strip.childElementCount;
        sectionRoot.append(heading, carousel);
        mediaRoot.appendChild(sectionRoot);
      });

      projectShell.classList.toggle("has-multiple-media", mediaCount > 1);

      requestAnimationFrame(() => {
        mediaRoot.querySelectorAll("video[autoplay]").forEach((video) => {
          video.play().catch(() => {});
        });
      });

      const firstValue = (key) => items.map((item) => item.dataset[key]).find(Boolean) || "";
      const configuredMeta = configured.meta || {};
      const fields = [
        ["Medium", configuredMeta.medium || firstValue("medium")],
        ["Year", configuredMeta.year || firstValue("year")],
        ["Size", configuredMeta.size || firstValue("size")],
        ["Credit", configuredMeta.credit || firstValue("credit")]
      ].filter((field) => field[1]);

      metaNode.innerHTML = fields.map(([label, value]) =>
        `<div><dt>${label}</dt><dd>${value}</dd></div>`).join("");

      const descriptions = [...new Set(items.map((item) => item.dataset.desc).filter(Boolean))];
      if (configured.descriptionHtml) {
        descriptionNode.innerHTML = configured.descriptionHtml;
      } else {
        descriptionNode.innerHTML = descriptions.map((text) => `<p>${text}</p>`).join("");
      }

      const hasDetails = fields.length || descriptionNode.textContent.trim();
      infoRoot.classList.toggle("is-empty", !hasDetails);

      const currentIndex = order.indexOf(currentId);
      const previousId = order[(currentIndex - 1 + order.length) % order.length];
      const nextId = order[(currentIndex + 1) % order.length];
      const projectHref = (id) => {
        const projectContent = (window.VISUAL_PROJECT_CONTENT || {})[id] || {};
        return projectContent.href || `visual-project.html?project=${encodeURIComponent(id)}`;
      };
      document.querySelector(".visual-project-prev").href = projectHref(previousId);
      document.querySelector(".visual-project-next").href = projectHref(nextId);

      document.addEventListener("keydown", (event) => {
        if (event.key === "ArrowLeft") window.location.href = document.querySelector(".visual-project-prev").href;
        if (event.key === "ArrowRight") window.location.href = document.querySelector(".visual-project-next").href;
        if (event.key === "Escape") window.location.href = "visual-design.html";
      });
    })
    .catch(showError);
})();
