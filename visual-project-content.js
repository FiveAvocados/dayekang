/*
 * Optional project-level overrides for the Visual Design viewer.
 *
 * To group works with different gallery titles, add an entry to GROUPS:
 * { id: "plastic-bags", titles: ["Plastic Bags Photography Book", "Plastic Bags", "Photography"] }
 *
 * To add a long project description, add HTML to CONTENT using the same id:
 * "plastic-bags": { descriptionHtml: "<p>First paragraph.</p><p>Second paragraph.</p>" }
 * To reuse media from another gallery item without merging the two projects:
 * "project-id": { mediaFromTitles: ["Another gallery title"] }
 * To add portfolio images that are not gallery cards, use additionalMedia:
 * "project-id": { additionalMedia: [{ src: "optimized image path", alt: "Example" }] }
 */
const qinqinEpisodeFrames = (episode) => Array.from({ length: 9 }, (_, index) => ({
  src: `assets/optimized/qinqin/episode-${episode}-${String(index + 1).padStart(2, "0")}.webp`,
  alt: `Episode ${episode}, frame ${index + 1}`
}));

window.VISUAL_PROJECT_GROUPS = [
  {
    id: "plastic-bags",
    title: "Plastic Bags",
    titles: ["Plastic Bags Photography Book", "Plastic Bags", "Photography"]
  }
];
window.VISUAL_PROJECT_CONTENT = {
  "qinqin-hou": {
    mediaSections: [
      { title: "Episode 1", ariaLabel: "Episode 1 storyboard frames", media: qinqinEpisodeFrames(1) },
      { title: "Episode 2", ariaLabel: "Episode 2 storyboard frames", media: qinqinEpisodeFrames(2) },
      { title: "Episode 3", ariaLabel: "Episode 3 storyboard frames", media: qinqinEpisodeFrames(3) }
    ]
  },
  "experimental-typography": {
    additionalMediaPosition: "before",
    meta: {
      medium: "Poster series, Photoshop",
      year: "2016",
      size: "A2 and A3",
      credit: "Made by Daye Kang"
    },
    descriptionHtml: "<p>A series on the visual qualities of mass in letterforms, from metallic and liquid surfaces to letters built from shapes found in everyday life.</p>",
    additionalMedia: [
      { src: "assets/optimized/visual/experimental-typography-01.webp", alt: "Experimental Typography poster mockup, metallic letterforms" },
      { src: "assets/optimized/visual/experimental-typography-02.webp", alt: "Experimental Typography poster mockup, flowing letterforms" },
      { src: "assets/optimized/visual/experimental-typography-03.webp", alt: "Experimental Typography poster mockup, dimensional letterforms" },
      { src: "assets/optimized/visual/experimental-typography-04.webp", alt: "Experimental Typography poster mockup, everyday found shapes" }
    ]
  },
  "typography-books": {
    meta: {
      medium: "Typography study, Illustrator and InDesign",
      year: "2024",
      size: "Letter",
      credit: "Designed and printed by Daye Kang"
    },
    descriptionHtml: "<p>A study of the Didot typeface, printed as a book.</p>",
    additionalMedia: [
      { src: "assets/optimized/visual/typography-books-02.webp", alt: "Typography Books, Didot type study spread" }
    ]
  },
  "graphic-poster": {
    meta: {
      medium: "Posters and book, Illustrator, Photoshop, and InDesign",
      year: "2013",
      size: "Book A4",
      credit: "Designed, printed, and bound by Daye Kang"
    },
    descriptionHtml: "<p>A graphic design study printed as posters and collected into a hand-bound book.</p>",
    additionalMedia: [
      { src: "assets/optimized/visual/graphic-poster-01.webp", alt: "Graphic Poster displayed on a concrete wall" },
      { src: "assets/optimized/visual/graphic-poster-02.webp", alt: "Graphic Poster hand-bound book cover" },
      { src: "assets/optimized/visual/graphic-poster-03.webp", alt: "Graphic Poster hand-bound book spread" }
    ]
  },
  "coca-cola-building": {
    title: "Coca-Cola Building",
    meta: {
      medium: "Poster series, Photoshop and Illustrator",
      year: "2014",
      size: "A2",
      credit: "Made by Daye Kang"
    },
    descriptionHtml: "<p>Photographs of the building in Los Angeles, cropped and rearranged into streamlined forms.</p>",
    additionalMedia: [
      { src: "assets/optimized/visual/coca-cola-building-02.webp", alt: "Coca-Cola Building poster series displayed together" }
    ]
  },
  "good-boy": {
    replaceMedia: true,
    mediaLayout: "horizontal-strip",
    meta: {
      medium: "3D animation, Maya",
      year: "2015",
      size: "1920 × 1080 · 1 minute",
      credit: "Creator (personal project) · Modeling, rigging, animation, rendering"
    },
    descriptionHtml: "<p>This project follows a boy who would rather go on a picnic than sit in class. His body stays in the classroom while his head runs off to play outside.</p>",
    additionalMedia: [
      { src: "assets/optimized/good-boy/hero.webp", alt: "Good Boy animation still, the boy and his floating head" },
      { src: "assets/optimized/good-boy/pull.webp", alt: "Good Boy animation still, the boy reaching for his head" },
      { src: "assets/optimized/good-boy/s1.webp", alt: "Good Boy animation still, classroom scene" },
      { src: "assets/optimized/good-boy/s3.webp", alt: "Good Boy animation still, picnic sequence" },
      { src: "assets/optimized/good-boy/s4.webp", alt: "Good Boy animation still, outdoor sequence" }
    ]
  }
};
