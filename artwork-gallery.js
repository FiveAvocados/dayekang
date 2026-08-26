(function () {
  window.ARTWORK_PROJECT_LINKS = true;

  const arts = [...document.querySelectorAll(".gallery .art")];
  const filterButtons = [...document.querySelectorAll(".artwork-filter")];
  const filterStatus = document.querySelector(".artwork-filter-status");

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

  const categoriesFor = (art) => {
    const text = `${art.dataset.title || ""} ${art.dataset.medium || ""}`.toLowerCase();
    const categories = new Set();
    if (/animation|video/.test(text)) categories.add("visual-storytelling");
    if (/installation/.test(text)) categories.add("installation");
    if (/photography|photograph|photoshoot/.test(text)) categories.add("photography");
    if (/illustration|drawing|watercolor|pencil|collage/.test(text)) categories.add("illustration");
    if (/graphic design|digital artwork|typography|poster|experimental graphics/.test(text)) categories.add("graphic-design");
    if (!categories.size) categories.add("graphic-design");
    return categories;
  };

  const projects = new Map();
  arts.forEach((art) => {
    const id = projectIdFor(art);
    const categories = categoriesFor(art);
    art.dataset.project = id;

    if (!projects.has(id)) {
      projects.set(id, { representative: art, categories });
      return;
    }

    const project = projects.get(id);
    categories.forEach((category) => project.categories.add(category));
    art.dataset.projectDuplicate = "true";
    art.hidden = true;
  });

  const projectCards = [...projects.values()];
  projectCards.forEach(({ representative, categories }) => {
    representative.dataset.categories = [...categories].join(" ");

    const link = document.createElement("a");
    link.className = "art-project-link";
    link.href = `visual-project.html?project=${encodeURIComponent(representative.dataset.project)}`;
    link.setAttribute("aria-label", `Open ${representative.dataset.title || "visual design"} project`);
    while (representative.firstChild) link.appendChild(representative.firstChild);
    representative.appendChild(link);
  });

  const loadGalleryVideo = (video) => {
    if (!video || video.getAttribute("src") || !video.dataset.src) return;
    video.src = video.dataset.src;
    video.load();
    if (!video.closest(".art")?.hidden) video.play().catch(() => {});
  };

  const galleryVideos = [...document.querySelectorAll(".gallery video[data-src]")];
  if ("IntersectionObserver" in window) {
    const videoObserver = new IntersectionObserver((entries, observer) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        loadGalleryVideo(entry.target);
        observer.unobserve(entry.target);
      });
    }, { rootMargin: "600px 0px" });
    galleryVideos.forEach((video) => videoObserver.observe(video));
  } else {
    galleryVideos.forEach(loadGalleryVideo);
  }

  const applyFilter = (button) => {
    const filter = button.dataset.filter;
    let shown = 0;

    projectCards.forEach(({ representative }) => {
      const categories = representative.dataset.categories.split(" ");
      const visible = filter === "all" || categories.includes(filter);
      representative.hidden = !visible;
      if (visible) {
        shown += 1;
        representative.classList.add("in");
      }

      const video = representative.querySelector("video");
      if (video) {
        if (visible && video.getAttribute("src")) video.play().catch(() => {});
        else video.pause();
      }
    });

    filterButtons.forEach((item) => {
      const active = item === button;
      item.classList.toggle("is-active", active);
      item.setAttribute("aria-pressed", String(active));
    });

    if (filterStatus) {
      const label = filter === "all" ? "all categories" : button.textContent.trim();
      filterStatus.textContent = `${shown} ${shown === 1 ? "project" : "projects"} shown for ${label}.`;
    }
  };

  filterButtons.forEach((button) => button.addEventListener("click", () => applyFilter(button)));
  const activeButton = filterButtons.find((button) => button.classList.contains("is-active")) || filterButtons[0];
  if (activeButton) applyFilter(activeButton);
})();
