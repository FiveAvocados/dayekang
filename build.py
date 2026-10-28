# Build script — generates all HTML pages. Images/PDFs reference LOCAL assets/ paths;
# assets_manifest.txt maps each local file to its source URL (downloaded by download_assets.sh).
import os, html

ROOT = os.path.dirname(os.path.abspath(__file__))
W = lambda name, content: open(os.path.join(ROOT, name), 'w').write(content)
MED = "https://static.wixstatic.com/media/"

# ---------------- asset registry ----------------
MANIFEST = {}  # local name -> source url

def _ext(wix_id):
    return os.path.splitext(wix_id.replace("~mv2", ""))[1] or ".png"

def A(name, wix_id, mode="fill", w=1280, h=840):
    """Register the original Wix asset and return its local path.

    Resizing belongs in the local optimization step. Downloading a Wix
    ``/v1/fit`` or ``/v1/fill`` derivative here permanently discards detail
    before the responsive website has a chance to size the image.
    """
    local = f"{name}{_ext(wix_id)}"
    url = MED + wix_id
    MANIFEST[local] = url
    return "assets/" + local

def PDF(name, url):
    MANIFEST[f"pdf/{name}"] = url
    return f"assets/pdf/{name}"

def V(name, wix_video_id):
    """Wix background video -> local mp4."""
    MANIFEST[f"video/{name}.mp4"] = f"https://video.wixstatic.com/video/{wix_video_id}/480p/mp4/file.mp4"
    return f"assets/video/{name}.mp4"

def arrow_row(a, b):
    return f'<div class="arrow-row">{a}<span class="arr2">&#8594;</span>{b}</div>'

def video_tag(path, cls=""):
    c = f' class="{cls}"' if cls else ""
    return f'<video{c} src="{path}" autoplay muted loop playsinline></video>'

# publication PDFs + CV
# CV = letter-size PDF generated from website/cv.html (source: Application CV/html_source/DayeKang_CV_v1_original.html)
# via headless chromium --print-to-pdf. NOT in the wix manifest — do not let the asset downloader overwrite it.
CV = "assets/pdf/DayeKang_CV.pdf?v=20261013"
PDF_THEMEVIZ = PDF("ThemeViz_CSCW25.pdf", "https://www.dayekang.info/_files/ugd/f4a835_7c199c01ef344bb0a711c80095e8215c.pdf")
PDF_HORMONE  = PDF("HormoneHealth_CHI25.pdf", "https://www.dayekang.info/_files/ugd/f4a835_e6d9a9e550be4aea9e197be522689d0f.pdf")
PDF_CSCW24   = PDF("UXRCollab_CSCW24.pdf", "https://www.dayekang.info/_files/ugd/f4a835_f1c471fb4c014d40b3915c81a48651a1.pdf")
PDF_TOONNOTE = PDF("ToonNote_CHI21.pdf", "https://www.dayekang.info/_files/ugd/f4a835_e2336fed6e5340d2a5ffdce1e2fd139c.pdf")
PDF_HEYTEDDY = PDF("HeyTeddy_IMWUT19.pdf", "https://www.dayekang.info/_files/ugd/f4a835_813a3ecec0c64db58d86ee0da30505dc.pdf")
PDF_CHOCO    = PDF("Chocolate_DIS19.pdf", "https://www.dayekang.info/_files/ugd/f4a835_565b5f2b321b4a2881bd633c51797129.pdf")

NAV = [
    ("publications.html", "Publications"),
    ("ux-projects.html", "UX Projects"),
    ("visual-design.html", "Visual Design"),
    ("teaching.html", "Teaching"),
]

def page(title, active, body, desc="Daye Kang — designer and HCI researcher. Ph.D. candidate at Cornell University Information Science.", body_class="", head_extra=""):
    ACT = ' class="active"'
    nav_items = "\n        ".join(
        f'<li><a href="{f}?v=20260820-full-width-nav"{ACT if f == active else ""}>{t}</a></li>' for f, t in NAV
    )
    brand_class = "brand home-brand"
    brand_content = ('<span class="brand-name">Daye Kang</span>'
                     '<span class="brand-role">Designer · Researcher</span>')
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<link rel="icon" href="favicon.svg?v=2" type="image/svg+xml">
<meta name="description" content="{desc}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Source+Serif+4:ital,opsz,wght@0,8..60,400;0,8..60,500;1,8..60,400&family=Inter:ital,wght@0,300;0,400;0,500;0,600;0,700;0,800;0,900;1,400;1,600&display=swap" rel="stylesheet">
{head_extra}
  <link rel="stylesheet" href="style.css?v=20261015-portfolio-projects">
</head>
<body{f' class="{body_class}"' if body_class else ''}>
<header>
  <div class="nav">
    <a class="{brand_class}" href="index.html?v=20260820-full-width-nav">{brand_content}</a>
    <button class="nav-toggle" aria-label="Menu" onclick="document.querySelector('nav').classList.toggle('open')">&#9776;</button>
    <nav>
      <ul>
        {nav_items}
      </ul>
    </nav>
  </div>
</header>
{body}
<footer>
  <div class="foot">
    <div class="kicker">Get in touch</div>
    <a class="big-link" href="mailto:dk564@cornell.edu">dk564@cornell.edu</a>
    <div class="foot-row">
      <div>&copy; 2026 Daye Kang &mdash; Ithaca, NY</div>
      <div>
        <a href="{CV}" target="_blank" rel="noopener">CV</a>
        <a href="https://www.dayekang.com" target="_blank" rel="noopener">dayekang.com</a>
      </div>
    </div>
  </div>
</footer>
<script src="site-nav.js?v=20260823-video-header"></script>
<script>
document.documentElement.classList.add('js');
const _io = new IntersectionObserver(es => es.forEach(e => {{
  if (e.isIntersecting) {{ e.target.classList.add('in'); _io.unobserve(e.target); }}
}}), {{ threshold: .07 }});
document.querySelectorAll('.reveal').forEach(el => _io.observe(el));
</script>
</body>
</html>
"""

# ================= INDEX =================
PORTRAIT = A("portrait", "f4a835_bada0c4f923c4b598b1052f08f6bba7e~mv2.png", "fill", 900, 1026)
# Organic profile: portrait blob (front) + nature video blob (behind), matching the original site.
NATURE_VID = "assets/optimized/video/nature2.mp4"
NATURE_POSTER = "assets/optimized/video/nature2-poster.jpg"
# Blob clip-paths (objectBoundingBox 0..1). Recreated from the original organic masks.
PPATH = ("M 0.44068,0.00890 C 0.34289,0.02506 0.24120,0.06355 0.17565,0.12501 C 0.11011,0.18647 0.05210,0.30778 0.02670,0.39708 C 0.00130,0.48638 -0.01011,0.60912 0.01523,0.68899 C 0.04056,0.76886 0.11117,0.85264 0.18673,0.90150 C 0.26229,0.95036 0.39447,0.99056 0.49245,0.99758 C 0.59044,1.00460 0.72650,0.98536 0.80558,0.94584 C 0.88466,0.90631 0.96891,0.81382 0.99190,0.74794 C 1.01489,0.68205 0.97697,0.59644 0.95078,0.52974 C 0.92460,0.46303 0.82968,0.38948 0.82654,0.32664 C 0.82341,0.26380 0.93627,0.18093 0.93099,0.13285 C 0.92572,0.08476 0.87088,0.04259 0.79325,0.02296 C 0.71562,0.00334 0.53847,-0.00726 0.44068,0.00890 Z")
NPATH = ("M 0.34851,0.00316 C 0.27940,0.01305 0.20972,0.05224 0.16283,0.11113 C 0.11594,0.17002 0.07757,0.29357 0.05236,0.37512 C 0.02715,0.45668 -0.00904,0.55341 0.00360,0.62620 C 0.01624,0.69900 0.07715,0.77920 0.13217,0.83490 C 0.18718,0.89060 0.27970,0.95446 0.35107,0.97797 C 0.42245,1.00147 0.51327,1.00803 0.58297,0.98334 C 0.65266,0.95864 0.72992,0.87916 0.79126,0.82200 C 0.85259,0.76485 0.93954,0.68824 0.97035,0.62235 C 1.00115,0.55646 1.00839,0.47409 0.98583,0.40585 C 0.96326,0.33762 0.88904,0.24796 0.82784,0.19141 C 0.76664,0.13485 0.67520,0.07846 0.59931,0.04866 C 0.52341,0.01885 0.41762,-0.00673 0.34851,0.00316 Z")

news = [
    ("Mar 2026", """I will attend CHI’26 to co-organize the Feminist HCI meet-up “<a href="https://feminist-hci.github.io/eastasia/" target="_blank" rel="noopener">Legitimizing, Developing, and Sustaining Feminist HCI in East Asia: Challenges and Opportunities</a>” and attend the following workshops. See you in Barcelona!
      <ul>
        <li><a href="https://chi26relationshipai.myportfolio.com/" target="_blank" rel="noopener">Toward Relationship-Centered Care with AI: Designing for Human Connections in Healthcare</a></li>
        <li><a href="https://ai-tools-for-thought.github.io/workshop/" target="_blank" rel="noopener">Tools for Thought: Understanding, Protecting, and Augmenting Human Cognition with Generative AI — From Vision to Implementation</a></li>
        <li><a href="https://vischi.org/" target="_blank" rel="noopener">Visual Storytelling Beyond the Human: Co-Creation, Culture, and Futures</a></li>
      </ul>"""),
    ("Oct 2025", '<span class="badge">🏅 Best Paper Honorable Mention Award</span> at CSCW’25 — “ThemeViz: Understanding the Effect of Human-AI Collaboration in Theme Development with an LLM-enhanced Interactive Visual System.”'),
    ("Jun 2025", """I will attend DIS 2025 workshops. See you at DIS!
      <ul>
        <li><a href="https://dis25designknowledgeinai.myportfolio.com/" target="_blank" rel="noopener">Design Knowledge in AI: Navigating Temporality and Continuity</a> — Examining the Effects of Human-AI Collaboration in Creative Visual Imagery</li>
        <li><a href="https://beatricevincenzi.com/byob-workshop-dis25.html" target="_blank" rel="noopener">Bring Your Own Biodata (BYOB): Feminist, Corporeal and Collective Approaches to Datafied Bodies</a> — Exploring New Sensemaking Methods to Understand Complex Lived Experiences with PCOS Data</li>
      </ul>"""),
    ("Jun 2025", "“ThemeViz: Understanding the Effect of Human-AI Collaboration in Theme Development with an LLM-enhanced Interactive Visual System” got accepted to CSCW 2025!"),
    ("Mar 2025", '<span class="badge">🏆 Best Paper Award</span> at CHI’25 — “Towards Hormone Health: An Autoethnography of Long-Term Holistic Tracking to Manage PCOS.”'),
    ("Jan 2025", "“Towards Hormone Health: An Autoethnography of Long-Term Holistic Tracking to Manage PCOS” has been conditionally accepted to CHI 2025. I thank all of my wonderful collaborators!"),
    ("Nov 2024", "Attending CSCW 2024 in Costa Rica to present my work “Challenges and Opportunities for Tool Adoption in Industrial UX Research Collaborations.”"),
    ("Nov 2024", "I passed my Candidacy exam!"),
    ("May 2024", 'Sharing “LLM-embedded interactive visual system for iterative theme refinement” at the CHI 2024 workshop <a href="https://sites.google.com/view/llmsindatawork/home" target="_blank" rel="noopener">LLMs as Research Tools: Applications and Evaluations in HCI Data Work</a>.'),
    ("Mar 2024", "The “Challenges and Opportunities for Tool Adoption in Industrial UX Research Collaborations” paper was accepted to CSCW’24."),
]
news_html = "\n".join(
    f'      <li class="reveal"><span class="date">{d}</span><span class="what">{t}</span></li>' for d, t in news
)

index_body = f"""
<main>
  <section class="hero wrap">
    <div class="hero-grid">
      <aside class="hero-side">
        <div class="portrait-organic reveal">
          <video class="po-nature" src="{NATURE_VID}" poster="{NATURE_POSTER}" preload="auto" autoplay muted loop playsinline aria-hidden="true"></video>
          <img class="po-portrait" src="{PORTRAIT}" alt="Portrait of Daye Kang">
          <svg class="po-defs" width="0" height="0" aria-hidden="true" focusable="false">
            <defs>
              <clipPath id="poPortraitClip" clipPathUnits="objectBoundingBox"><path d="{PPATH}"/></clipPath>
              <clipPath id="poNatureClip" clipPathUnits="objectBoundingBox"><path d="{NPATH}"/></clipPath>
            </defs>
          </svg>
        </div>
        <div class="hero-links">
          <div class="hl-text">
            <a href="{CV}" target="_blank" rel="noopener">CV</a><span class="hl-sep">|</span><a href="https://scholar.google.com/citations?user=LQQPHtcAAAAJ" target="_blank" rel="noopener">Google Scholar</a><span class="hl-sep">|</span><a class="hl-email" href="mailto:dk564@cornell.edu" aria-label="Email"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="2.6" y="4.8" width="18.8" height="14.4" rx="1.6"/><path d="M3.4 6.2 12 13l8.6-6.8"/></svg></a>
            <a class="hl-linkedin" href="https://www.linkedin.com/in/daye-kang-98475a128/" target="_blank" rel="noopener" aria-label="LinkedIn" hidden><svg viewBox="0 0 448 512" fill="currentColor" aria-hidden="true"><path d="M100.28 448H7.4V148.9h92.88zM53.79 108.1C24.09 108.1 0 83.5 0 53.8a53.79 53.79 0 0 1 107.58 0c0 29.7-24.1 54.3-53.79 54.3zM447.9 448h-92.68V302.4c0-34.7-.7-79.2-48.29-79.2-48.29 0-55.69 37.7-55.69 76.7V448h-92.78V148.9h89.08v40.8h1.3c12.4-23.5 42.69-48.3 87.88-48.3 94 0 111.28 61.9 111.28 142.3V448z"/></svg></a>
          </div>
        </div>
        <a class="selected-jump selected-jump-desktop is-hidden" href="#selected-work">
          <span class="selected-jump-label">See<br>selected<br>work</span>
          <span class="selected-jump-arrow" aria-hidden="true">↓</span>
        </a>
      </aside>
      <div class="hero-copy">
        <div class="bio bio-primary">
          <p>Welcome to my website. My name is Daye Kang. My research interests lie at the intersection of <strong>design</strong>, <strong>human-computer interaction (HCI)</strong>, and <strong>human-AI interaction</strong>.</p>
          <p>People have access to more data than ever, but more data does not lead to better understanding. My research agenda is to design human-AI interaction that makes data easier to use, understand, and communicate.</p>
          <p>I use qualitative methods, including co-design and first-person studies, to understand people’s contexts, then design and evaluate systems that combine visualization and AI to support data sensemaking.</p>
        </div>
        <div class="bio bio-secondary">
          <p>My research has been published at top-tier HCI conferences such as ACM CHI and CSCW, and has received a Best Paper Award and a Best Paper Honorable Mention Award.</p>
          <p>I am currently a Ph.D. candidate in Information Science at Cornell University, advised by <a class="academic-link" href="https://mjung.infosci.cornell.edu/" target="_blank" rel="noopener">Malte Jung</a>. Previously, I received my MS in Industrial Design from KAIST, advised by <a class="academic-link" href="https://make.kaist.ac.kr/andrea" target="_blank" rel="noopener">Andrea Bianchi</a>, after receiving a BFA in Visual Communication Design at Hongik University.</p>
          <p class="pron">My name is pronounced Da-Ye [da ye].</p>
          <p class="job-market">I am on the academic job market for the 2026–27 cycle.</p>
        </div>
        <a class="selected-work-link" href="#selected-work">
          <span>See selected work</span>
          <span class="selected-work-link-arrow" aria-hidden="true">↓</span>
        </a>
      </div>
      <a class="selected-jump selected-jump-mobile is-hidden" href="#selected-work">
        <span class="selected-jump-label">See<br>selected<br>work</span>
        <span class="selected-jump-arrow" aria-hidden="true">↓</span>
      </a>
    </div>
  </section>

  <section class="section selected-work-section" id="selected-work" aria-labelledby="selected-work-title">
    <div class="wrap">
      <div class="sec-head reveal">
        <h2 id="selected-work-title">Selected work</h2>
      </div>

      <div class="selected-work-groups">
        <section class="selected-group reveal" aria-labelledby="selected-publications-title">
          <div class="selected-group-head">
            <h3 id="selected-publications-title">Publications</h3>
          </div>
          <ol class="selected-pub-list">
            <li>
              <div class="selected-pub-conference">CSCW 2025</div>
              <p>ThemeViz: Understanding the Effect of Human-AI Collaboration in Theme Development with an LLM-enhanced Interactive Visual System</p>
              <div class="selected-pub-award-row"><span class="selected-award">Best Paper Honorable Mention Award</span></div>
              <div class="selected-pub-links"><a href="assets/pdf/ThemeViz_CSCW25.pdf" target="_blank" rel="noopener">PDF</a><a href="https://dl.acm.org/doi/10.1145/3757675" target="_blank" rel="noopener">DOI</a></div>
            </li>
            <li>
              <div class="selected-pub-conference">CHI 2025</div>
              <p>Towards Hormone Health: An Autoethnography of Long-Term Holistic Tracking to Manage PCOS</p>
              <div class="selected-pub-award-row"><span class="selected-award">Best Paper Award</span></div>
              <div class="selected-pub-links"><a href="assets/pdf/HormoneHealth_CHI25.pdf" target="_blank" rel="noopener">PDF</a><a href="https://dl.acm.org/doi/abs/10.1145/3706598.3713619" target="_blank" rel="noopener">DOI</a></div>
            </li>
            <li>
              <div class="selected-pub-conference">CHI 2021</div>
              <p>ToonNote: Improving Communication in Computational Notebooks Using Interactive Data Comics</p>
              <div class="selected-pub-award-row" aria-hidden="true"></div>
              <div class="selected-pub-links"><a href="assets/pdf/ToonNote_CHI21.pdf" target="_blank" rel="noopener">PDF</a><a href="https://dl.acm.org/doi/10.1145/3411764.3445434" target="_blank" rel="noopener">DOI</a></div>
            </li>
          </ol>
          <a class="selected-more" href="publications.html?v=20260820-full-width-nav"><span class="selected-more-label">See all publications</span><span class="selected-more-arrow" aria-hidden="true">→</span></a>
        </section>

        <section class="selected-group selected-design-group reveal" aria-labelledby="selected-design-title">
          <div class="selected-group-head">
            <h3 id="selected-design-title">Design Projects</h3>
          </div>
          <div class="design-branches">
            <article class="design-branch">
              <h4>UX Design</h4>
              <div class="design-image-grid">
                <img class="design-project-image" src="assets/optimized/ux_lexia.webp" alt="Lexia in Wonderland UX project" loading="lazy">
              </div>
              <div class="design-project-details">
                <h5>Lexia in Wonderland</h5>
                <div class="design-project-awards" aria-label="Awards">
                  <span class="selected-award">2017 Adobe Design Achievement Awards Semifinalist</span>
                  <span class="selected-award">2017 KSDS Excellence Award</span>
                  <span class="selected-award">2017 Hongik Excellence Graduation Work</span>
                </div>
              </div>
              <a class="selected-more" href="ux-projects.html?v=20260820-full-width-nav"><span class="selected-more-label">See all UX projects</span><span class="selected-more-arrow" aria-hidden="true">→</span></a>
            </article>

            <article class="design-branch">
              <h4>Visual Storytelling</h4>
              <div class="design-project-entry">
                <div class="design-image-grid">
                  <img class="design-project-image" src="assets/optimized/art_22.webp" alt="Still image from the QinQin Hou animation" loading="lazy">
                </div>
                <div class="design-project-details">
                  <h5>QinQin Hou</h5>
                  <div class="design-project-awards" aria-label="Awards">
                    <span class="selected-award">Excellence Award, Times Young Creative Awards</span>
                  </div>
                </div>
              </div>
              <a class="selected-more" href="visual-design.html?v=20260820-full-width-nav"><span class="selected-more-label">See all visual design works</span><span class="selected-more-arrow" aria-hidden="true">→</span></a>
            </article>

            <article class="design-branch">
              <h4>Graphic Design</h4>
              <div class="design-image-grid">
                <img class="design-project-image" src="assets/optimized/art_02.webp" alt="Black-and-white graphic design study" loading="lazy">
              </div>
              <div class="design-project-details">
                <h5>Digital Artwork</h5>
              </div>
            </article>
          </div>
        </section>
      </div>
    </div>
  </section>

  <section class="section">
    <div class="wrap">
      <div class="sec-head reveal">
        <h2>News</h2>
      </div>
      <ul class="news news-scroll">
{news_html}
      </ul>
    </div>
  </section>

</main>
<script src="visual-design-prefetch.js?v=20260825-gallery-fast"></script>
"""
W("index.html", page("Daye Kang — Designer & HCI Researcher", "index.html", index_body))

# ================= PUBLICATIONS =================
pubs = [
    dict(venue="CSCW 2025", award="Best Paper Honorable Mention Award",
         thumb=A("pub_themeviz_teaser", "f4a835_5bf2731eb386491ca9c3a4e8683428b9~mv2.png", "fill", 1000, 726),
         title="ThemeViz: Understanding the Effect of Human-AI Collaboration in Theme Development with an LLM-enhanced Interactive Visual System",
         authors="<b>Daye Kang</b>, Zhuolun Han, Jiahe Tian, Muhan Zhang, and Jeff Rzeszotarski",
         abs="This paper explores the potential role of AI, e.g., large language models (LLMs), in supporting theme development in thematic analysis. While prior applications of AI in qualitative data analysis have focused on supporting coding, we investigate whether LLMs can effectively contribute as collaborators in the more abstract and conceptual phases of qualitative analysis, specifically theme development. We designed ThemeViz, an interactive system that uses GPT-4 to generate and visualize multiple versions of themes based on user input while allowing researchers to maintain control through manual coding and theme development.",
         links=[("PDF", PDF_THEMEVIZ), ("DOI", "https://dl.acm.org/doi/10.1145/3757675")]),
    dict(venue="CHI 2025", award="Best Paper Award",
         thumb=A("pub_hormone", "f4a835_c97dfad2927340bb81ef92ed2e62a4d8~mv2.png", "fill", 1000, 726),
         title="Towards Hormone Health: An Autoethnography of Long-Term Holistic Tracking to Manage PCOS",
         authors="<b>Daye Kang</b>, Jingjin Li, Gilly Leshed, Jeff Rzeszotarski and Xi Lu",
         abs="Polycystic ovary syndrome (PCOS) is a common hormonal disorder affecting 11–13% of women of reproductive age, characterized by a wide range of symptoms that varies among individuals. While self-tracking tools help PCOS patients to monitor their symptoms and find personalized treatment, they often focus on regular periods of healthy women with inadequate support for the personalization and long-term holistic tracking necessary for managing complex chronic conditions like PCOS. The first author (who has PCOS) conducted an autoethnographic study of holistic self-tracking over ten months; our results highlight the challenges of personalized, holistic, long-term tracking and provide design implications for tracking tools that are more inclusive and sustainable.",
         links=[("PDF", PDF_HORMONE), ("DOI", "https://dl.acm.org/doi/abs/10.1145/3706598.3713619")]),
    dict(venue="CSCW 2024", award=None,
         thumb=A("pub_cscw24", "f4a835_a822c19ae2ba497dab34c883228418d7~mv2.jpg", "fill", 1000, 726),
         title="Challenges and Opportunities for Tool Adoption in Industrial UX Research Collaborations",
         authors="<b>Daye Kang</b>, and Jeff Rzeszotarski",
         abs="Qualitative UX research practitioners analyze data to comprehend users’ needs and synthesize implications for future design. Working with multiple stakeholders is inevitable in modern product development, and in industry, coordination and collaboration add pressures to already laborious qualitative data analysis tasks. We investigate how multi-stakeholder collaboration specifically affects industry qualitative data analysis practices — the challenges practitioners face, limitations of current tools, and opportunities for computer-supported cooperative work.",
         links=[("PDF", PDF_CSCW24), ("DOI", "https://dl.acm.org/doi/10.1145/3686982")]),
    dict(venue="CHI 2021", award=None,
         thumb=A("pub_toonnote", "f4a835_7b122c4e1e744d669f1f52a2e450edca~mv2.png", "fill", 1000, 726),
         title="ToonNote: Improving Communication in Computational Notebooks Using Interactive Data Comics",
         authors="<b>Daye Kang</b>, Tony Ho, Nicolai Marquardt, Bilge Mutlu, Andrea Bianchi",
         abs="ToonNote is a novel technique for representing computational notebooks in the form of interactive data comics. ToonNote provides a high-level, curated narrative of the dataset in Comic View. Readers can focus on data storytelling, and not be hindered by code, unnecessary outputs, or markdown — and can switch back to the Notebook View when needed.",
         links=[("PDF", PDF_TOONNOTE), ("GitHub", "https://github.com/tho121/ComicConverter/"), ("DOI", "https://dl.acm.org/doi/10.1145/3411764.3445434")]),
    dict(venue="IMWUT 2019", award=None,
         thumb=A("pub_heyteddy", "f4a835_f4fc46d0192f43faa070ddff1de83a5d~mv2.jpg", "fill", 1000, 726),
         title="HeyTeddy: Conversational Test-Driven Development for Physical Computing",
         authors="Yoonji Kim, Youngkyung Choi, <b>Daye Kang</b>, Minkyeong Lee, Tek-Jin Nam, Andrea Bianchi",
         abs="Physical computing is a complex activity that consists of different but tightly coupled tasks: programming and assembling hardware for circuits. We propose a general-purpose prototyping tool based on conversation. HeyTeddy guides users during hardware assembly by providing additional information on requests or by interactively presenting the assembly steps to build a circuit.",
         links=[("Video", "https://youtu.be/GUtUtIBBJ74"), ("PDF", PDF_HEYTEDDY), ("DOI", "https://doi.org/10.1145/3369838")]),
    dict(venue="DIS 2019", award=None,
         thumb=A("pub_chocolate", "f4a835_fd21a5dc108648a39621985f9df651d8~mv2.jpg", "fill", 1000, 726),
         title="Designing Internal Structure of Chocolate and Its Effect on Food Texture",
         authors="Yujin Lee, Jee Bin Yim, <b>Daye Kang</b>, Hyeon-Beom Yi, Daniel Saakes",
         abs="We explored the effects of the internal structure on the texture of chocolate by designing, building, and testing chocolates with different internal structures and internal chocolate percentage. Multiple layers of patterned chocolate were stacked as a fabrication method; each layer was fabricated using a silicone mold made from a 3D-printed model.",
         links=[("PDF", PDF_CHOCO), ("DOI", "https://dl.acm.org/doi/10.1145/3301019.3323896")]),
    dict(venue="KSDS 2017", award=None,
         thumb=A("pub_lexia", "f4a835_19619498ec1448248541516b7679a67b~mv2.png", "fill", 1000, 726),
         title="Lexia in Wonderland: Korean Education Service for Children with Dyslexia",
         authors="<b>Daye Kang</b>, Hye-Ryeong Kim, Ji-Hae Lee, Jae Young Yun",
         abs="Treating dyslexia during childhood is very important. In Korea, this is not the case since the condition is not well understood, and there is a limited number of medical centers that offer treatment for it. We propose an education app for dyslexic children ages 5–10 in Korea that helps children through active learning — teaching Korean phonics using ‘nonwords’ in a fun and engaging way so they can be treated at home.",
         links=[("Project", "lexiainwonderland.html"),
                ("English translation", "assets/papers/lexia-in-wonderland-english-translation.pdf")]),
    dict(venue="KSDS 2017", award=None,
         thumb=A("pub_nudge", "f4a835_e2efb323288c47bdb4926afd3b024a76~mv2.png", "fill", 1000, 726),
         title="Nudge Design to Increase Physical Activities for Hospitalized Children",
         authors="<b>Daye Kang</b>, Hye-Min Choi, Ka-Hyun Kim, Younjoon Lee",
         abs="Hospitalized children are often asked to regularly walk in the hallway to stay active. However, the hallway is usually dull and empty. We created wallpapers and floor footprint stickers that use nudge design to be fun and engaging — footprint stickers promote walking and leg stretches while the wallpaper contains stories that add fun moments.",
         links=[("Project", "nudgedesign.html"),
                ("English translation", "assets/papers/nudge-design-english-translation.pdf")]),
]

def pub_html(p):
    EXT = ' target="_blank" rel="noopener"'
    award = f'<span class="award-pill">{p["award"]}</span>' if p["award"] else ""
    links = "".join(f'<a href="{u}"{EXT if u.startswith("http") or u.startswith("assets/") else ""}>{t}</a>' for t, u in p["links"])
    return f"""    <article class="pub reveal">
      <div class="thumb"><img src="{p['thumb']}" alt="{html.escape(p['title'])}" loading="lazy"></div>
      <div>
        <div class="venue"><span>{p['venue']}</span>{award}</div>
        <h3>{p['title']}</h3>
        <div class="authors">{p['authors']}</div>
        <p class="abs">{p['abs']}</p>
        <div class="links">{links}</div>
      </div>
    </article>"""

pubs_body = f"""
<main>
  <div class="wrap">
    <div class="bleed ux-video-hero publication-video-hero reveal">
      {video_tag("assets/optimized/video/tiger.mp4")}
      <div class="ux-video-hero-copy"><h1>Publications</h1></div>
    </div>
    <div class="page-head">
      <div class="kicker">Peer-reviewed research</div>
      <h1>Publications</h1>
      <p class="lede">My research agenda is to design human-AI interaction that makes data easier to use, understand, and communicate. People have access to more data than ever, but more data does not lead to better understanding. Data sits fragmented across tools, separated from the personal and social contexts that gave it meaning. When those contexts are lost, people struggle to see patterns, to build a coherent account of what the data says, or to pass that account on to someone else.</p>
      <p class="lede">I see this gap as a design problem. More capable AI models do not by themselves decide whether people can make sense of data. How information is organized, connected, represented, and made available for interaction matters as well.</p>
      <p class="lede">I pursue this across three domains: reflective practice in qualitative data analysis, managing chronic conditions with health tracking tools, and data storytelling through comics.</p>
    </div>
{chr(10).join(pub_html(p) for p in pubs)}
  </div>
</main>
"""
W("publications.html", page("Publications — Daye Kang", "publications.html", pubs_body, body_class="video-hero-page"))

# ================= CARD helper =================
def card(href, img_path, tag, title, desc, extra_class=""):
    card_class = f"card reveal {extra_class}".strip()
    return f"""      <a class="{card_class}" href="{href}">
        <span class="arrow">&#8599;</span>
        <div class="frame"><img src="{img_path}" alt="{html.escape(title)}" loading="lazy"></div>
        <div class="pad">
          <h3>{title}</h3>
          <span class="tag">{tag}</span>
          <p>{desc}</p>
        </div>
      </a>"""

def placeholder_card(href, tag, title, desc):
    return f"""      <a class="card reveal" href="{href}">
        <span class="arrow">&#8599;</span>
        <div class="frame project-placeholder" role="img" aria-label="{html.escape(title)} representative image to be added"></div>
        <div class="pad">
          <h3>{title}</h3>
          <span class="tag">{tag}</span>
          {f'<p>{desc}</p>' if desc else ''}
        </div>
      </a>"""

# ================= UX RESEARCH =================
ux_body = f"""
<main class="ux-projects-page">
  <div class="wrap">
    <div class="bleed ux-video-hero reveal">
      {video_tag("assets/optimized/video/shark.mp4")}
      <div class="ux-video-hero-copy"><h1>UX Projects</h1></div>
    </div>
    <div class="cards" id="ux-project-list">
{card("themeviz.html", "assets/banner10.png?v=20261013", "Human-AI collaboration, Data Sensemaking", "ThemeViz", "LLM-Enhanced Visual System for Theme Development")}
{card("mindful-journaling.html", "assets/originals/mindful/mindful-workflow.png?v=20260824", "Project page", "Mindful", "AI-Assisted Journaling for Reflection", "mindful-card")}
{placeholder_card("toonnote.html", "Project page", "ToonNote", "Interactive Data Comics for Computational Notebooks")}
{placeholder_card("pmos-comics.html", "Interactive comics · Series", "PMOS.Comics",
      "A project series exploring personal health data through interactive comics. Full project description coming soon.")}
{card("lexiainwonderland.html", A("ux_lexia", "f4a835_eb3d171453984c1d8ab28fd7eeabb5dc~mv2.png", "fill", 1280, 840),
      "Education · Gamification", "Lexia in Wonderland",
      "A Korean education app for imaginative, dyslexic children that wraps scientifically proven treatment methods in a fun adventure.")}
{card("nudgedesign.html", A("ux_nudge", "f4a835_e2efb323288c47bdb4926afd3b024a76~mv2.png", "fill", 1280, 840),
      "Nudge design · Health", "Nudge Design for Hospitalized Children",
      "Footprint stickers and story wallpapers that turn a dull hallway into a place to play and encourage hospitalized children to walk and stretch.")}
{card("mylittlehero.html", "assets/optimized/ux_mlh.webp",
      "Game · Family engagement", "My Little Hero",
      "A digital game that facilitates communication between children who are hospitalized long term and their family members through play.")}
{card("bookrecommendation.html", A("ds_bookrec", "f4a835_ddc7400150214afebb07f52a82c092f8~mv2.png", "fill", 1280, 840),
      "Recommendation · R Shiny", "Book Recommendation System",
      "We designed and developed a book recommendation system that recommends the next few books for our target users based on their own reading tastes.")}
{card("sunshine.html", "assets/optimized/sun_hero.webp",
      "IoT · Multisensory", "Sunshine",
      "An IoT digital window controlled from a smartphone app that changes the view with matching scents, sounds, and breeze.")}
{card("tomorrow.html", A("ux_tomorrow", "f4a835_ff310f1c911b4a118aa6d9619bfe9afa~mv2.png", "fill", 1280, 840),
      "Education · Social impact", "Tomorrow",
      "Teaching coding and French to refugee children in France through donated devices, classic children’s books, and block coding.")}
    </div>
  </div>
</main>
"""
W("ux-projects.html", page("UX Projects — Daye Kang", "ux-projects.html", ux_body, body_class="video-hero-page"))

# Preserve the former URL while keeping the public page name aligned with the menu.
W("ux-research.html", """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex">
<meta http-equiv="refresh" content="0; url=ux-projects.html">
<link rel="canonical" href="https://www.dayekang.com/ux-projects.html">
<title>UX Projects — Daye Kang</title>
<script>location.replace("ux-projects.html" + location.search + location.hash);</script>
</head>
<body><p><a href="ux-projects.html">Continue to UX Projects</a></p></body>
</html>
""")

# Keep old bookmarks working without restoring the removed Data Science section.
W("data-science.html", """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex">
<meta http-equiv="refresh" content="0; url=ux-projects.html">
<link rel="canonical" href="ux-projects.html">
<title>UX Projects — Daye Kang</title>
<link rel="icon" href="favicon.svg?v=2" type="image/svg+xml">
<script>window.location.replace("ux-projects.html" + window.location.search + window.location.hash);</script>
</head>
<body>
<p><a href="ux-projects.html">Continue to UX Projects</a></p>
</body>
</html>
""")

# ================= ARTWORK =================
# (id, title, description) — collected from the original Wix gallery expand view, in gallery order
ART = [
    # (id, title, medium, year, size, credit, description)
    ("f4a835_97ff5f36332f46c1822fb6d57f876002~mv2.gif", "Cancer", "3D animation — 3D Maya", "2016", "3 minutes", "Directed by Daye Kang", "This animation is about a character who fights against cancer and finds her true self."),
    ("f4a835_718d23aa99a04c0faf1b5f03d2628ec5~mv2.png", "Digital Artwork", "Digital artwork — Photoshop", "2016", "", "Made by Daye Kang", ""),
    ("f4a835_74498a1bf82046548560c2d2fae2830f~mv2.jpg", "Humanize Technology", "Graphic design — Photoshop", "2018", "", "Made by Daye Kang", "This illustration was used as a book cover for a personal portfolio."),
    ("f4a835_15da437160a74ee185354c91637d5f21~mv2.gif", "Punky Music", "Clay animation — Clay, Adobe After Effects", "2014", "1280×720 px · 45 seconds", "Directed by Daye Kang · Music: Crying Nuts", "I wanted to express the bright, innocent craziness of punk rock music with this animation."),
    ("f4a835_f185a992116c4a8988ae7028f36367a9~mv2.png", "Walnuts", "Drawing — Pencil", "2012", "545×394 mm", "Drawn by Daye Kang", ""),
    ("f4a835_ce1878f5b183448eb74da8b0263ca2af~mv2.jpg", "How to be Bohemian", "Digital illustration — Photoshop", "2014", "", "Made by Daye Kang", "This illustration is one of five drawings created for an article titled ‘How to Be Bohemian’ for a subculture project. This character was designed to convey a free spirit."),
    ("f4a835_ce1938a91813421eb6ecf661ec31b6c4~mv2.png", "Experimental Typography", "Poster series, Photoshop", "2016", "A2 and A3", "Made by Daye Kang", "A series on the visual qualities of mass in letterforms, from metallic and liquid surfaces to letters built from shapes found in everyday life."),
    ("f4a835_882ab0a0cfac472b900d61a841a04541~mv2.jpg", "Dancer", "Digital photoshoot", "2014", "", "Photoshoot by Daye Kang", ""),
    ("f4a835_a2f26fdd27624a8f90ecf1f203c28e28~mv2.png", "Digital Artwork", "Digital artwork — Photoshop", "2016", "", "Made by Daye Kang", ""),
    ("f4a835_3d7a9b8d2f47402280bcd2f0b60dad89~mv2.png", "Experimental Typography", "Experimental typography — Photoshop", "2016", "", "Made by Daye Kang", ""),
    ("f4a835_f0947f4994334987977a4678473f4777~mv2.png", "Experimental Typography", "Experimental typography — Photoshop", "2016", "", "Made by Daye Kang", ""),
    ("f4a835_96b4b99d90484a06b9967c14ce4c08c7~mv2.png", "Experimental Typography", "Experimental typography — Photoshop", "2016", "", "Made by Daye Kang", ""),
    ("f4a835_1929adc1141f49fe9eec44a9de75a9a0~mv2.jpg", "Disassembled walls", "Drawing — Pencil, color pencil, tracing paper", "2013", "30×40 cm", "Drawn by Daye Kang", "There is a small room at my school where you can listen to different music. There are lots of trees near this building. I thought it would be great if this room’s walls were disassembled so I could enjoy music while lying on the sofa in the sun. I used tracing paper to give depth to the drawing and make it slightly blurry, creating a dreamy atmosphere. I drew clouds, shadows, birds, a sofa, and a girl on the tracing paper."),
    ("f4a835_d3e8574835574d8aa5794a7f80e2fa52~mv2.png", "Digital Artwork", "Digital artwork — Photoshop", "2016", "", "Made by Daye Kang", ""),
    ("VIDEO:f4a835_3db1c57433f6444eb267addf251ee757", "Hue:", "Interactive installation", "2018", "", "Made by Daye Kang, Juyeon Kim", "Hue: is an interactive installation that displays the time. We designed this installation based on the aesthetics of the city and the desert. When a person approaches the clock, it rotates and displays the current time."),
    ("f4a835_f06e24334ce94e0a95d8c051fc3078c7~mv2.jpg", "Dancer with lights", "Digital photoshoot", "2014", "", "Photoshoot by Daye Kang", "The lights and lingering shapes were captured using long-exposure photography."),
    ("f4a835_2151f087af2a42678cebbb23bea2e140~mv2.png", "Good Boy", "3D animation, Maya", "2015", "1920 × 1080 · 1 minute", "Creator (personal project) · Modeling, rigging, animation, rendering", "This project follows a boy who would rather go on a picnic than sit in class. His body stays in the classroom while his head runs off to play outside."),
    ("f4a835_f2b5e5075cc94e5ea644435a6ea8f25a~mv2.png", "Illustration", "Digital illustration — Photoshop", "2020", "90×50 mm", "Drawn by Daye Kang", "I designed this illustration for a client who is a traveler and writer. I focused on emphasizing the client’s love of winter sports and outdoor activities. Lines and different locations also represent his love of travel."),
    ("f4a835_ae2e827b40084d7d80d93460d59f14ae~mv2.jpg", "Graphic Poster", "Posters and book, Illustrator, Photoshop, and InDesign", "2013", "Book A4", "Designed, printed, and bound by Daye Kang", "A graphic design study printed as posters and collected into a hand-bound book."),
    ("f4a835_8aeda735d1374112bf3dc48097b29eff~mv2.png", "Zarathustra", "Drawing &amp; collage on aluminum foil — Pen, Crayons, Oil paper, Black paper", "2013", "50×40 cm", "Made by Daye Kang", "This artwork depicts members of the music club ‘Zarathustra’ gathered in the club room."),
    ("f4a835_03cddcf2da7f4ec3ad97c348b39ab7e7~mv2.jpg", "Conversation", "Drawing — Watercolor, Pen", "2013", "15×10 cm", "Made by Daye Kang", ""),
    ("LOCAL_VIDEO:assets/optimized/video/art_31.mp4", "QinQin Hou", "3D animation — Maya, Illustrator, After Effects", "2016", "1920×1080 · 3 minutes", "Director · 3D background modeling · Character design · Animation — Daye Kang", "This animation is one of three episodes in a commercial created for the candy company QinQinHou. Each episode depicts a moment when a character loses their voice. After eating the candy, their voice returns and the fun continues. The animation received an Award for Excellence from the Times Young Creative Awards."),
    ("f4a835_e4f6cb606cd3481799170e7049942898~mv2.jpg", "Coca-Cola Building", "Poster series, Photoshop and Illustrator", "2014", "A2", "Made by Daye Kang", "Photographs of the building in Los Angeles, cropped and rearranged into streamlined forms."),
    ("f4a835_6e2ed7df286f40a0b56c94cef5039731~mv2.png", "Experimental Typography", "Experimental typography", "2016", "A3", "Made by Daye Kang", "I focused on liquid and flowing forms."),
    ("f4a835_9b04971e5940440ea13193f70b3b0f8d~mv2.png", "Plastic Bags Photography Book", "Photography book — Photography, A4 paper, staples", "2016", "20×20 cm", "Made by Daye Kang", "This book is a collection of photographs exploring the expressiveness of plastic bags in photography. I chose a plastic bag as the main subject after being inspired by the movie ‘American Beauty.’ The book was made using A4 paper, which was folded to create square pages. Instead of using an open-spine binding, I chose staples because I wanted to explore the book’s raw exterior."),
    ("f4a835_a5602d2b85a944b9919d6c06f91e036e~mv2.jpg", "Plastic Bags", "Photography", "2016", "A4", "Made by Daye Kang", ""),
    ("f4a835_e116429e3f694d518bc762d1943468be~mv2.png", "Shape of the body", "Photography", "2014", "", "Photoshoot by Daye Kang", "I explored the graphical forms of the naked body and the effects of lighting on the muscles."),
    ("f4a835_460e9d4effae459b86759b83b110aeb8~mv2.png", "Experimental Graphics", "Digital artwork — Photoshop", "2016", "", "Made by Daye Kang", ""),
    ("f4a835_ac641b8b476742478d76ef61d91d9031~mv2.png", "Photography", "Photography", "2016", "", "Photoshoot by Daye Kang", "I explored the graphical forms of plastic bags."),
    ("f4a835_30d2277513364ceb8bc6e1a8b86cb72d~mv2.png", "Digital Illustration", "Digital illustration — Photoshop", "2016", "20×10 cm", "Drawn by Daye Kang", "I drew my friend while traveling in Shanghai."),
    ("LOCAL_IMAGE:assets/optimized/visual/typography-books-01.webp", "Typography Books", "Typography study, Illustrator and InDesign", "2024", "Letter", "Designed and printed by Daye Kang", "A study of the Didot typeface, printed as a book."),
]
ART_GALLERY_DIMS = {
    1: (916, 436), 2: (1200, 1716), 3: (1200, 1237), 4: (896, 484),
    5: (1200, 1200), 6: (1200, 1653), 7: (1200, 1699), 8: (1200, 1352),
    9: (1200, 1709), 10: (1200, 1698), 11: (1200, 1709), 12: (1098, 1560),
    13: (1200, 1751), 14: (1200, 1200), 15: (800, 450), 16: (1200, 1217),
    17: (1200, 940), 18: (1061, 591), 19: (959, 1354), 20: (1200, 887),
    21: (1200, 892), 22: (1200, 663), 23: (1200, 1600), 24: (1200, 1698),
    25: (1200, 957), 26: (1200, 691), 27: (1200, 1162), 28: (1200, 1698),
    29: (820, 1008), 30: (1200, 768), 31: (1200, 800),
}

def _art_item(n, i, title, medium, year, size, credit, desc):
    width, height = ART_GALLERY_DIMS[n]
    gallery_version = "?v=20260825-gallery-fast"
    if i.startswith("LOCAL_IMAGE:"):
        full = i[len("LOCAL_IMAGE:"):]
        thumb = full.replace("assets/optimized/visual/", "assets/optimized/gallery/")
        media = (f'<img src="{thumb}" data-full-src="{full}" alt="{html.escape(title)}" '
                 f'width="{width}" height="{height}" decoding="async" loading="lazy">')
    elif i.startswith("LOCAL_VIDEO:"):
        video_path = i[len("LOCAL_VIDEO:"):]
        poster = f"assets/optimized/gallery/art_{n:02d}-1200.webp{gallery_version}"
        media = (f'<video data-src="{video_path}" data-full-src="{video_path}" poster="{poster}" '
                 f'preload="none" autoplay muted loop playsinline width="{width}" height="{height}"></video>')
    elif i.startswith("VIDEO:"):
        video_path = V(f"art_{n:02d}", i[6:]).replace("assets/video/", "assets/optimized/video/")
        poster = f"assets/optimized/gallery/art_{n:02d}-1200.webp{gallery_version}"
        media = (f'<video data-src="{video_path}" data-full-src="{video_path}" poster="{poster}" '
                 f'preload="none" autoplay muted loop playsinline width="{width}" height="{height}"></video>')
    else:
        A(f"art_{n:02d}", i, "fit", 800, 1200)
        thumb = f"assets/optimized/gallery/art_{n:02d}-1200.webp{gallery_version}"
        full = f"assets/optimized/art_{n:02d}.webp?v=20260821-original"
        priority = ' loading="eager" fetchpriority="high"' if n in {1, 7, 17, 23} else ' loading="lazy"'
        media = (f'<img src="{thumb}" data-full-src="{full}" alt="{html.escape(title)}" '
                 f'width="{width}" height="{height}" decoding="async"{priority}>')
    attrs = (f' data-title="{html.escape(title, quote=True)}" data-medium="{html.escape(medium, quote=True)}"'
             f' data-year="{html.escape(year, quote=True)}" data-size="{html.escape(size, quote=True)}"'
             f' data-credit="{html.escape(credit, quote=True)}" data-desc="{html.escape(desc, quote=True)}"')
    return (f'      <div class="art reveal"{attrs}>'
            f'{media}<div class="art-overlay"><span>{html.escape(title)}</span></div></div>')

art_imgs = "\n".join(_art_item(n, *item) for n, item in enumerate(ART, 1))
art_body = f"""
<main>
  <div class="wrap">
    <div class="bleed artwork-video-hero reveal">
      {video_tag("assets/optimized/video/bird4.mp4")}
      <div class="ux-video-hero-copy"><h1>Visual Design</h1></div>
    </div>
    <div class="artwork-filters" role="group" aria-label="Filter visual design projects by category">
      <button class="artwork-filter is-active" type="button" data-filter="all" aria-pressed="true">All</button>
      <button class="artwork-filter" type="button" data-filter="visual-storytelling" aria-pressed="false">Visual storytelling</button>
      <button class="artwork-filter" type="button" data-filter="graphic-design" aria-pressed="false">Graphic design</button>
      <button class="artwork-filter" type="button" data-filter="installation" aria-pressed="false">Installation</button>
      <button class="artwork-filter" type="button" data-filter="illustration" aria-pressed="false">Illustration</button>
      <button class="artwork-filter" type="button" data-filter="photography" aria-pressed="false">Photography</button>
    </div>
    <p class="artwork-filter-status" aria-live="polite">All 31 projects shown.</p>
    <div class="gallery">
{art_imgs}
    </div>
  </div>
</main>
<div class="lightbox" id="lightbox" role="dialog" aria-label="Enlarged artwork">
  <button class="lb-nav prev" id="lb-prev" aria-label="Previous artwork">&#8249;</button>
  <button class="lb-nav next" id="lb-next" aria-label="Next artwork">&#8250;</button>
  <button class="lb-close" id="lb-close" aria-label="Close artwork">&times;</button>
  <figure>
    <img src="" alt="Artwork enlarged">
    <figcaption>
      <strong id="lb-title"></strong>
      <div class="lb-meta" id="lb-meta"></div>
      <p id="lb-desc"></p>
    </figcaption>
  </figure>
</div>
<script src="visual-project-content.js?v=20261027-qinqin-consistent"></script>
<script src="artwork-gallery.js?v=20261015-portfolio-projects"></script>
<script>
if (!window.ARTWORK_PROJECT_LINKS) (function() {{
  const lb = document.getElementById('lightbox');
  const lbImg = lb.querySelector('img');
  const lbTitle = document.getElementById('lb-title');
  const lbDesc = document.getElementById('lb-desc');
  const lbMeta = document.getElementById('lb-meta');
  const arts = [...document.querySelectorAll('.gallery .art')];
  const filterButtons = [...document.querySelectorAll('.artwork-filter')];
  const filterStatus = document.querySelector('.artwork-filter-status');
  const categoriesFor = (art) => {{
    const text = `${{art.dataset.title || ''}} ${{art.dataset.medium || ''}}`.toLowerCase();
    const categories = new Set();
    if (/animation|video/.test(text)) categories.add('visual-storytelling');
    if (/installation/.test(text)) categories.add('installation');
    if (/photography|photograph|photoshoot/.test(text)) categories.add('photography');
    if (/illustration|drawing|watercolor|pencil|collage/.test(text)) categories.add('illustration');
    if (/graphic design|digital artwork|typography|poster|experimental graphics/.test(text)) categories.add('graphic-design');
    if (!categories.size) categories.add('graphic-design');
    return [...categories];
  }};
  arts.forEach(art => {{ art.dataset.categories = categoriesFor(art).join(' '); }});
  const imageItems = arts.filter(art => art.querySelector('img'));
  const visibleItems = () => imageItems.filter(art => !art.hidden);
  let cur = 0;
  const show = (i) => {{
    const items = visibleItems();
    if (!items.length) return;
    cur = (i + items.length) % items.length;
    const art = items[cur];
    lbImg.src = art.querySelector('img').src;
    lbTitle.textContent = art.dataset.title || '';
    const fields = [['Medium', art.dataset.medium], ['Year', art.dataset.year], ['Size', art.dataset.size], ['Credit', art.dataset.credit]];
    lbMeta.innerHTML = fields.filter(f => f[1]).map(f =>
      '<div><span class="k">' + f[0] + '</span><span class="v">' + f[1] + '</span></div>').join('');
    lbDesc.textContent = art.dataset.desc || '';
    lbDesc.style.display = art.dataset.desc ? '' : 'none';
  }};
  imageItems.forEach(art => {{
    art.addEventListener('click', () => {{
      show(visibleItems().indexOf(art));
      lb.classList.add('open');
      document.body.style.overflow = 'hidden';
    }});
  }});
  filterButtons.forEach(button => {{
    button.addEventListener('click', () => {{
      const filter = button.dataset.filter;
      let shown = 0;
      arts.forEach(art => {{
        const visible = filter === 'all' || art.dataset.categories.split(' ').includes(filter);
        art.hidden = !visible;
        if (visible) {{
          shown += 1;
          art.classList.add('in');
        }}
        const video = art.querySelector('video');
        if (video) {{
          if (visible) video.play().catch(() => {{}});
          else video.pause();
        }}
      }});
      filterButtons.forEach(item => {{
        const active = item === button;
        item.classList.toggle('is-active', active);
        item.setAttribute('aria-pressed', String(active));
      }});
      filterStatus.textContent = `${{shown}} ${{shown === 1 ? 'project' : 'projects'}} shown for ${{button.textContent}}.`;
    }});
  }});
  document.getElementById('lb-prev').addEventListener('click', e => {{ e.stopPropagation(); show(cur - 1); }});
  document.getElementById('lb-next').addEventListener('click', e => {{ e.stopPropagation(); show(cur + 1); }});
  document.addEventListener('keydown', e => {{
    if (!lb.classList.contains('open')) return;
    if (e.key === 'ArrowLeft') show(cur - 1);
    if (e.key === 'ArrowRight') show(cur + 1);
  }});
  const close = () => {{ lb.classList.remove('open'); document.body.style.overflow = ''; }};
  lb.querySelector('figure').addEventListener('click', e => e.stopPropagation());
  document.getElementById('lb-close').addEventListener('click', e => {{ e.stopPropagation(); close(); }});
  lb.addEventListener('click', close);
  document.addEventListener('keydown', e => {{ if (e.key === 'Escape') close(); }});
}})();
</script>"""
visual_design_preloads = """<link rel="preload" as="image" href="assets/optimized/gallery/art_01-1200.webp?v=20260825-gallery-fast" fetchpriority="high">
<link rel="preload" as="image" href="assets/optimized/gallery/art_07-1200.webp?v=20260825-gallery-fast" fetchpriority="high">
<link rel="preload" as="image" href="assets/optimized/gallery/art_17-1200.webp?v=20260825-gallery-fast" fetchpriority="high">
<link rel="preload" as="image" href="assets/optimized/gallery/art_23-1200.webp?v=20260825-gallery-fast" fetchpriority="high">"""
W("visual-design.html", page("Visual Design — Daye Kang", "visual-design.html", art_body,
                             body_class="video-hero-page", head_extra=visual_design_preloads))

# Preserve the former URL while keeping the public page name aligned with the menu.
W("artwork.html", """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex">
<meta http-equiv="refresh" content="0; url=visual-design.html">
<link rel="canonical" href="https://www.dayekang.com/visual-design.html">
<title>Visual Design — Daye Kang</title>
<script>location.replace("visual-design.html" + location.search + location.hash);</script>
</head>
<body><p><a href="visual-design.html">Continue to Visual Design</a></p></body>
</html>
""")

# ================= QINQIN HOU — permanent CV URL =================
# Public filename contract: do not rename qinqinhou.html.
qinqin_body = """
<main class="qinqin-page">
  <div class="qinqin-player-wrap">
    <!-- Add the final MP4 as a source here once the original video file is available. -->
    <video class="qinqin-player" controls preload="none" poster="assets/optimized/art_22.webp" aria-label="QinQin Hou animation">
      Your browser does not support HTML video.
    </video>
  </div>
  <div class="wrap">
    <section class="qinqin-storyboards" aria-labelledby="qinqin-storyboards-title">
      <h2 id="qinqin-storyboards-title">Episode storyboards</h2>
      <section class="qinqin-episode" aria-labelledby="qinqin-episode-1">
        <h3 id="qinqin-episode-1">Episode 1</h3>
        <div class="qinqin-frame-strip" role="region" aria-label="Episode 1 storyboard frames" tabindex="0">
          <figure class="qinqin-frame"><img src="assets/optimized/qinqin/episode-1-01.webp" alt="Episode 1, frame 1" width="1700" height="956" decoding="async" loading="lazy"></figure>
          <figure class="qinqin-frame"><img src="assets/optimized/qinqin/episode-1-02.webp" alt="Episode 1, frame 2" width="900" height="506" decoding="async" loading="lazy"></figure>
          <figure class="qinqin-frame"><img src="assets/optimized/qinqin/episode-1-03.webp" alt="Episode 1, frame 3" width="900" height="506" decoding="async" loading="lazy"></figure>
          <figure class="qinqin-frame"><img src="assets/optimized/qinqin/episode-1-04.webp" alt="Episode 1, frame 4" width="900" height="506" decoding="async" loading="lazy"></figure>
          <figure class="qinqin-frame"><img src="assets/optimized/qinqin/episode-1-05.webp" alt="Episode 1, frame 5" width="900" height="506" decoding="async" loading="lazy"></figure>
          <figure class="qinqin-frame"><img src="assets/optimized/qinqin/episode-1-06.webp" alt="Episode 1, frame 6" width="900" height="506" decoding="async" loading="lazy"></figure>
          <figure class="qinqin-frame"><img src="assets/optimized/qinqin/episode-1-07.webp" alt="Episode 1, frame 7" width="900" height="506" decoding="async" loading="lazy"></figure>
          <figure class="qinqin-frame"><img src="assets/optimized/qinqin/episode-1-08.webp" alt="Episode 1, frame 8" width="900" height="506" decoding="async" loading="lazy"></figure>
          <figure class="qinqin-frame"><img src="assets/optimized/qinqin/episode-1-09.webp" alt="Episode 1, frame 9" width="900" height="506" decoding="async" loading="lazy"></figure>
        </div>
      </section>
      <section class="qinqin-episode" aria-labelledby="qinqin-episode-2">
        <h3 id="qinqin-episode-2">Episode 2</h3>
        <div class="qinqin-frame-strip" role="region" aria-label="Episode 2 storyboard frames" tabindex="0">
          <figure class="qinqin-frame"><img src="assets/optimized/qinqin/episode-2-01.webp" alt="Episode 2, frame 1" width="1700" height="956" decoding="async" loading="lazy"></figure>
          <figure class="qinqin-frame"><img src="assets/optimized/qinqin/episode-2-02.webp" alt="Episode 2, frame 2" width="900" height="506" decoding="async" loading="lazy"></figure>
          <figure class="qinqin-frame"><img src="assets/optimized/qinqin/episode-2-03.webp" alt="Episode 2, frame 3" width="900" height="506" decoding="async" loading="lazy"></figure>
          <figure class="qinqin-frame"><img src="assets/optimized/qinqin/episode-2-04.webp" alt="Episode 2, frame 4" width="900" height="506" decoding="async" loading="lazy"></figure>
          <figure class="qinqin-frame"><img src="assets/optimized/qinqin/episode-2-05.webp" alt="Episode 2, frame 5" width="900" height="506" decoding="async" loading="lazy"></figure>
          <figure class="qinqin-frame"><img src="assets/optimized/qinqin/episode-2-06.webp" alt="Episode 2, frame 6" width="900" height="506" decoding="async" loading="lazy"></figure>
          <figure class="qinqin-frame"><img src="assets/optimized/qinqin/episode-2-07.webp" alt="Episode 2, frame 7" width="900" height="506" decoding="async" loading="lazy"></figure>
          <figure class="qinqin-frame"><img src="assets/optimized/qinqin/episode-2-08.webp" alt="Episode 2, frame 8" width="900" height="506" decoding="async" loading="lazy"></figure>
          <figure class="qinqin-frame"><img src="assets/optimized/qinqin/episode-2-09.webp" alt="Episode 2, frame 9" width="900" height="506" decoding="async" loading="lazy"></figure>
        </div>
      </section>
      <section class="qinqin-episode" aria-labelledby="qinqin-episode-3">
        <h3 id="qinqin-episode-3">Episode 3</h3>
        <div class="qinqin-frame-strip" role="region" aria-label="Episode 3 storyboard frames" tabindex="0">
          <figure class="qinqin-frame"><img src="assets/optimized/qinqin/episode-3-01.webp" alt="Episode 3, frame 1" width="1700" height="956" decoding="async" loading="lazy"></figure>
          <figure class="qinqin-frame"><img src="assets/optimized/qinqin/episode-3-02.webp" alt="Episode 3, frame 2" width="900" height="506" decoding="async" loading="lazy"></figure>
          <figure class="qinqin-frame"><img src="assets/optimized/qinqin/episode-3-03.webp" alt="Episode 3, frame 3" width="900" height="506" decoding="async" loading="lazy"></figure>
          <figure class="qinqin-frame"><img src="assets/optimized/qinqin/episode-3-04.webp" alt="Episode 3, frame 4" width="900" height="506" decoding="async" loading="lazy"></figure>
          <figure class="qinqin-frame"><img src="assets/optimized/qinqin/episode-3-05.webp" alt="Episode 3, frame 5" width="900" height="506" decoding="async" loading="lazy"></figure>
          <figure class="qinqin-frame"><img src="assets/optimized/qinqin/episode-3-06.webp" alt="Episode 3, frame 6" width="900" height="506" decoding="async" loading="lazy"></figure>
          <figure class="qinqin-frame"><img src="assets/optimized/qinqin/episode-3-07.webp" alt="Episode 3, frame 7" width="900" height="506" decoding="async" loading="lazy"></figure>
          <figure class="qinqin-frame"><img src="assets/optimized/qinqin/episode-3-08.webp" alt="Episode 3, frame 8" width="900" height="506" decoding="async" loading="lazy"></figure>
          <figure class="qinqin-frame"><img src="assets/optimized/qinqin/episode-3-09.webp" alt="Episode 3, frame 9" width="900" height="506" decoding="async" loading="lazy"></figure>
        </div>
      </section>
    </section>
    <article class="qinqin-copy">
      <div class="kicker">3D Animation · 2016</div>
      <h1>QinQin Hou</h1>
      <div class="qinqin-award">Excellence Award, Times Young Creative Awards</div>
      <p class="qinqin-description">This animation is one of three episodes in a commercial created for the candy company QinQinHou. Each episode depicts a moment when a character loses their voice. After eating the candy, their voice returns and the fun continues. The animation received an Award for Excellence from the Times Young Creative Awards.</p>
      <dl class="meta-grid">
        <div><dt>Medium</dt><dd>3D animation — Maya, Illustrator, After Effects</dd></div>
        <div><dt>Format</dt><dd>1920×1080 · 3 minutes</dd></div>
        <div><dt>Credit</dt><dd>Director · 3D background modeling · Character design · Animation — Daye Kang</dd></div>
      </dl>
      <a class="back-home" href="visual-design.html">&larr; Back to Visual Design</a>
    </article>
  </div>
</main>
"""
W("qinqinhou.html", """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta http-equiv="refresh" content="0; url=visual-project.html?project=qinqin-hou">
<link rel="canonical" href="https://www.dayekang.com/visual-project.html?project=qinqin-hou">
<title>QinQin Hou — Daye Kang</title>
<script>location.replace("visual-project.html?project=qinqin-hou" + location.hash);</script>
</head>
<body><p><a href="visual-project.html?project=qinqin-hou">Continue to QinQin Hou</a></p></body>
</html>
""")

# ================= TEACHING =================
teaching_body = """
<main>
  <div class="wrap">
    <div class="page-head">
      <h1>Teaching</h1>
    </div>
    <div class="placeholder reveal">
      <div class="big">Coming soon</div>
      <p>Course pages and student work are being prepared.</p>
    </div>
  </div>
</main>
"""
# The teaching portfolio is maintained by hand because it contains student
# artifacts and interactive project links. Keep a future site rebuild from
# replacing it with the original placeholder.
teaching_path = os.path.join(ROOT, "teaching.html")
if not os.path.exists(teaching_path):
    W("teaching.html", page("Teaching — Daye Kang", "teaching.html", teaching_body))

# ================= DETAIL PAGES =================
def hero_img(name, wix_id, alt=""):
    """Full-bleed hero banner, edge to edge like the original site."""
    return f'<div class="bleed"><img src="{A(name, wix_id, "fit", 1600, 2000)}" alt="{html.escape(alt)}"></div>'

def detail(fname, title, kicker, meta, intro_html, sections, awards=None, back="ux-projects.html", hero=""):
    if awards:
        meta = list(meta) + [("Awards", awards.replace(" \u00b7 ", "<br>"))]
    meta_html = "".join(f"<div><dt>{k}</dt><dd>{v}</dd></div>" for k, v in meta)
    sec_html = ""
    nav_items = ['<a href="#intro">Intro</a>']
    for n, sec in enumerate(sections, 1):
        h, content = sec[0], sec[1]
        cls = (" " + sec[2]) if len(sec) > 2 and sec[2] else ""
        if h:
            sec_html += f'\n      <section class="dsec{cls}" id="s{n}"><h2 class="reveal">{h}</h2>\n{content}\n</section>\n'
            nav_items.append(f'<a href="#s{n}">{h}</a>')
        else:
            sec_html += content + "\n"
    side_nav = ""
    spy_js = ""
    kicker_html = "" if back == "ux-projects.html" else f'<div class="kicker">{kicker}</div>'
    if len(nav_items) >= 3:
        side_nav = f'<nav class="side-nav" aria-label="Page sections">{"".join(nav_items)}</nav>'
        spy_js = """
<script>
(function() {
  const secs = [document.getElementById('intro'), ...document.querySelectorAll('.dsec')].filter(Boolean);
  const links = [...document.querySelectorAll('.side-nav a')];
  const spy = () => {
    let cur = 0;
    secs.forEach((s, i) => { if (s.getBoundingClientRect().top < 160) cur = i; });
    links.forEach((l, i) => l.classList.toggle('on', i === cur));
  };
  document.addEventListener('scroll', spy, { passive: true });
  window.addEventListener('resize', spy);
  spy();
})();
</script>"""
    detail_script = {
        "lexiainwonderland.html": '<script src="lexia-layout.js?v=20261013-grammar"></script>',
        "nudgedesign.html": '<script src="nudge-layout.js?v=20261013-observation-equal-height"></script>',
    }.get(fname, "")
    body = f"""
{side_nav}
<main>
  <div class="wrap">
    <div class="page-head">
      {kicker_html}
      <h1>{title}</h1>
    </div>
    <article class="detail">
      <div id="intro">
        {intro_html}
        <dl class="meta-grid">{meta_html}</dl>
      </div>
      {hero}
      {sec_html}
      <a class="back-home" href="{back}">&larr; Back to projects</a>
    </article>
  </div>
</main>
{detail_script}
{spy_js}"""
    detail_body_class = {
        "lexiainwonderland.html": "legacy-ux-page lexia-page",
        "nudgedesign.html": "legacy-ux-page nudge-page",
        "themeviz.html": "themeviz-page",
        "mindful-journaling.html": "mindful-page",
    }.get(fname, "")
    detail_head = ({
        "lexiainwonderland.html": '<link rel="stylesheet" href="ux-layout-overrides.css?v=20261013-lexia-exhibition-grid">',
        "nudgedesign.html": '<link rel="stylesheet" href="ux-layout-overrides.css?v=20261013-nudge-observation-equal-height">',
    }.get(fname, ""))
    W(fname, page(
        f"{title} — Daye Kang",
        None,
        body,
        body_class=detail_body_class,
        head_extra=detail_head,
    ))

def dimg(name, wix_id, alt=""):
    return f'<img class="reveal" src="{A(name, wix_id, "fit", 1600, 2000)}" alt="{html.escape(alt)}" loading="lazy">'

def dimg_m(name, wix_id, alt=""):
    return f'<img class="reveal" src="{A(name, wix_id, "fit", 900, 1400)}" alt="{html.escape(alt)}" loading="lazy">'

def dimg_s(name, wix_id, alt=""):
    return f'<img src="{A(name, wix_id, "fit", 500, 700)}" alt="{html.escape(alt)}" loading="lazy">'

def row(cls, *items):
    c = f"figrow {cls}".strip()
    return f'<div class="{c}">{"".join(items)}</div>'

def cap(text):
    return f'<p class="caption">{text}</p>'

def quote(text):
    return f'<p class="pull-quote">{text}</p>'

def qa(who, *ps):
    body = "".join(f"<p>{p}</p>" for p in ps)
    return f'<div class="qa"><div class="who">{who}</div>{body}</div>'

def lcol(label, *imgs):
    """Labeled column for flow layouts (e.g., Wrong / Correct)."""
    return f'<div class="lcol"><div class="lcol-label">{label}</div>{"".join(imgs)}</div>'

def split(img_html, text_html):
    """Image left, text right (persona-style layout)."""
    return f'<div class="split"><div>{img_html}</div><div>{text_html}</div></div>'

def stack(*items):
    return f'<div class="vstack">{"".join(items)}</div>'

def int_card(img_html, num, name, role, *quotes):
    qs = "".join(f'<p class="q">{q}</p>' for q in quotes)
    return (f'<div class="int-card"><div class="int-head">{img_html}'
            f'<div><div class="int-name"><b>{num}</b> {name}</div><div class="int-role">{role}</div></div></div>{qs}</div>')

def sub_band(cls, *content):
    return f'<div class="banded {cls}">{"".join(content)}</div>'

def flow_center(label, img_html, caption=None):
    c = f'<p class="caption" style="margin-top:4px">{caption}</p>' if caption else ""
    return f'<div class="flow-center"><div class="lcol-label">{label}</div>{img_html}{c}<div class="flow-arrows" aria-hidden="true"><span>&#8601;</span><span>&#8600;</span></div></div>'

detail("bookrecommendation.html", "Book Recommendation System", "UX Projects",
    [("Keywords", "Recommendation, Collaborative Filtering, R Shiny App"),
     ("Members", "Eda Zhang, Radhika Kulkarni, Daye Kang, Eunhee Sung"),
     ("My contribution", "Collaborative Filtering, Exploratory Data Analysis, UI mockup"),
     ("Year", "2.2020 – 5.2020")],
    "<p>We designed and developed a book recommendation system that recommends the next few books for our target users based on their own reading tastes.</p>",
    [("Project Description",
      "<h3>Executive Summary</h3>"
      "<p>In this project, we designed and developed a book recommendation system that recommends the next few books for our target users based on their own reading tastes. Here is the current version of the app: <a href='https://edaxplor.shinyapps.io/book_v4/' target='_blank' rel='noopener'>edaxplor.shinyapps.io/book_v4</a>. The data sources we used came from the UCSD Book Graph website and a Book Recommender Project on Kaggle. Considering the scope of our project and our target users, mainly children younger than 15 years old and educators of children in that age group, we used two datasets from the websites: a book dataset containing the fantasy and children's book genres and a rating dataset with users' ratings of the books. Logistic and linear regression models were tested for overall model adequacy and showed some linear relationships between the variables.</p>"
      "<p>To figure out the best algorithm for our product, we analyzed and compared the datasets using both supervised and unsupervised learning. The results showed that the unsupervised learning methods performed better than the supervised learning methods. Among the different supervised learning techniques we implemented, the linear model, the fast and frugal tree, outperformed the other models, including the generalized linear model and the nonlinear XGBoost model. We included the details of our analysis in the model interpretation section. In terms of unsupervised learning, we found that the collaborative filtering clustering method fit the goal of our project best. Other clustering methods we implemented included dimensionality-reduction techniques with UMAP and K-means. Ultimately, we used the UBCF algorithm to make recommendations to our users based on their own book preferences, and we captured the main ideas of the books through TF-IDF analysis of their descriptions.</p>"
      "<p>As a result, a book recommender was developed as an R Shiny app with genre and rating filters. After users select their favorite genre and rate books that they have read, the model suggests three books. As a reference, a word cloud is also drawn to show which words are frequently used in each book.</p>"
      "<p>It is not easy to recommend a book to others because people spend money to buy a book and time to read it. There are some ways to help readers find the next book they might like, such as browsing best-selling books displayed by genre in bookstores or searching for and reading other people's reviews online. These resources might help people decide on a book they may like, but they do not always work. Since every person has their own reading tastes, picking a book they might like takes time. To save them time and make their decisions easier, the book recommendation system uses an algorithm that can save them the trouble of searching online, reading all the reviews, and comparing the results with their tastes.</p>"
      "<p>In this project, a book recommendation algorithm was built for two genres: children's books and fantasy books. Therefore, anyone who would like to read a new book, especially fantasy lovers, children, their parents, and educators who teach children under the age of 15, is a target user for this application.</p>"),
     ("Data Sources & Preprocessing",
      "<h3>Data Set</h3>"
      "<p>To develop the application, we used four datasets. The main dataset used to develop the model was the Genre dataset. The dataset was collected in late 2017 from goodreads.com, with several files updated in May 2019. It has 26 columns and 1,242 rows: book_id, authors, average_rating, goodreads_book_id, country_code, description, format, image_url, is_ebook, isbn, isbn13, language_code, link, num_pages, publication_year, publisher, ratings_count, series, similar_books, title, title_without_series, URL, and work_id.</p>"
      "<p>Next, three datasets contributed by Philipp Spachtholz on Kaggle were combined into one rating dataset: ‘ratings.csv’ (3 columns, 194,941 rows: book_id, user_id, rating), ‘book_tags.csv’ (3 columns, 999,912 rows: goodreads_book_id, tag_id, count), and ‘tags.csv’ (2 columns, 34,252 rows: tag_id, tag_name). The combined rating dataset has the same column, “book_id,” as the genre dataset, so the two datasets can be used together to build the book recommendation application.</p>"
      "<h3>Data Analysis</h3>"
      "<p>Review ratings can be biased because people tend to leave ratings when they are very satisfied or disappointed. Ratings are the most important values for a recommendation application because people receive suggestions for highly rated books first. Before creating the algorithm, we drew a distribution plot to check whether the average ratings in the dataset were biased. Figure 1 shows that the data is approximately normally distributed, with an average of 3.90, so the average ratings are not biased.</p>"
      + dimg_m("book_f01", "f4a835_1e8c6eb1186947beb41baba311d2d6a3~mv2.png", "Figure 1") + cap("Figure 1. Distribution plot of average rating")
      + "<p>Next, a logistic regression model was used because the response variable, genre, is binary. The model checks whether there is a relationship between the dependent variable, genre, and the independent variables: average rating, number of pages, publication year, rating count, text review count, and title length. Using the glm function in R, a model was obtained, as shown in Figure 2.</p>"
      + dimg_m("book_f02", "f4a835_72d25873a739483db730d7e096b3b46a~mv2.png", "Figure 2") + cap("Figure 2. Summary of logistic regression")
      + "<p>Since the z-values for the number of pages and title length variables are very small, the coefficients of the two variables are significant. This result explains the dataset well because the dependent variable consists of two genres. The average number of pages in children's books is not expected to be as high as that in adult books, and the average title length of children's books is 25% greater than that of fantasy books.</p>"
      "<p>Next, the model was checked against the normality assumption by examining the normal probability plot. Figure 3 shows the normal probability plot of the residuals, which follows an approximately normal distribution.</p>"
      + dimg_m("book_f03", "f4a835_7b69506c334140b1ba07dc67c0645b87~mv2.png", "Figure 3") + cap("Figure 3. Q-Q plot of residuals for logistic regression")
      + "<p>This dataset was intended for an online recommendation system, so the average rating of books was considered the most significant variable. A linear regression model was fitted with average rating as the outcome and the other variables as predictors to check their relationships with average rating. Since average rating is a numeric value, a multiple linear regression model was used.</p>"
      + dimg_m("book_f04", "f4a835_b8057d4d04a4435bb119dc3bab151712~mv2.png", "Figure 4") + cap("Figure 4. Summary of linear regression")
      + "<p>Since the p-value for the number of pages variable is very small, its coefficient is significant, suggesting that the number of pages has a linear relationship with the average rating. We then checked whether the model met the normality assumption by examining the normal probability plot in Figure 5. All of the points follow the straight line in the plot, indicating that the residuals follow a normal distribution.</p>"
      + dimg_m("book_f05", "f4a835_b9d1db0c381f40489a3a43219ae56aef~mv2.png", "Figure 5") + cap("Figure 5. Q-Q plot of residuals for linear regression")
      + "<h3>Preprocessing of Data</h3>"
      "<p>The data was processed to better suit the machine learning algorithms through binary encoding of categorical variables, scaling of variables, and removal of missing values and columns with NA values.</p>"),
     ("Collaborative Filtering",
      dimg_m("book_f06", "f4a835_7c9ba9fbc7d04fddb69064ac042d4fca~mv2.png", "Figure 6") + cap("Figure 6. The collaborative filtering process")
      + "<p>We chose collaborative filtering because it is widely used for recommendations. It assumes that if person A has the same opinion as person B on one issue, person A is more likely to share person B's opinion on a different issue than that of a randomly chosen person.</p>"
      "<p>Figure 6 illustrates how CF works. First, you create a matrix in a certain format, with columns representing items and rows representing users. You then put this matrix into CF algorithms to get recommendations. (Source: Item-Based Collaborative Filtering Recommendation Algorithms.) We followed three steps for the recommendation process, referencing the process from Kaggle's book recommendation example: data processing and exploration, finding user neighbors, and making recommendations.</p>"
      "<p>The first step is data processing and exploration. At this stage, we removed duplicate ratings and then removed users who had rated fewer than three books. We selected a subset of users to speed up calculations and explored the cleaned dataset. Titles with five or seven words had slightly higher ratings. After that, we looked at the top-rated and most popular books. Next, we created a matrix for the CF algorithm.</p>"
      + dimg_m("book_f07", "f4a835_d4aa8d7bc0f94d909af0449641dd8883~mv2.png", "Figure 7") + cap("Figure 7. Exploratory data analysis")
      + dimg_m("book_f08", "f4a835_ad170507101b4904bb52358b283972eb~mv2.png", "Figure 8") + cap("Figure 8. Top 10 top-rated books and top 10 popular books")
      + dimg_m("book_f09", "f4a835_fee45e5b22474325bd2333039f242f0a~mv2.png", "Figure 9") + cap("Figure 9. Matrix for UBCF")
      + "<p>The second step is finding user neighbors. At this stage, we found similar users by comparing the books they both liked. In this case, we set the current user as 794 and then found users who had rated the same books. We normalized the users' ratings and sorted the users according to similarity. For this, we used Pearson correlation. Figure 11 shows the similarities between the current user and 30 randomly selected users, plotted with qgraph.</p>"
      + dimg_m("book_f10", "f4a835_97a62dd71aee4699a24d270f277c5b25~mv2.png", "Figure 10") + cap("Figure 10. Process of finding user neighbors")
      + dimg_m("book_f11", "f4a835_0065ec963bcb4fba8173d97eed88ad23~mv2.png", "Figure 11") + cap("Figure 11. Similarities between users")
      + "<p>Finally, in step three, the algorithm recommends books that best fit the target user based on the preferences of similar users.</p>"
      + dimg_m("book_f12", "f4a835_85960a6abdb9440889115ce6213c006b~mv2.png", "Figure 12") + cap("Figure 12. Best recommendations for the user")),
     ("Model Interpretation and Explanation",
      "<h3>Supervised Learning</h3>"
      "<p>To select the most suitable techniques for our project, we implemented both supervised and unsupervised techniques to investigate how well they performed on the dataset. The datasets we used contain different types of data: categorical, interval, ratio, and text, with more categorical data than other types. Therefore, classification models fit our goal better.</p>"
      "<p>We implemented three types of classification models: Fast and Frugal decision tree analysis, XGBoost, and a generalized linear model. To measure the performance of each model, we created an ROC curve. As shown in Figure 13, all three supervised models performed poorly on the task, with only small differences between them. The result suggested that supervised learning might not be the best approach for our project.</p>"
      + dimg_m("book_f13", "f4a835_e3c78e7d2acd4a2cbd0c9b65161ddb34~mv2.png", "Figure 13") + cap("Figure 13. Performance ROC curve")
      + "<p>The result from the Fast and Frugal decision tree in Figure 14 indicated that publication year, number of pages, genre, and number of reviews were the most important variables in deciding whether a book would be recommended to a user.</p>"
      + dimg_m("book_f14", "f4a835_56fd54db89bd4cdbb8a5d4223478241b~mv2.png", "Figure 14") + cap("Figure 14. Result from the Fast and Frugal decision tree")
      + "<p>On the other hand, GLM and XGBoost identified rating count, number of pages, and text review count, along with publication year, as the top four important features in their models.</p>"
      + dimg_m("book_f15", "f4a835_694a101918f7463abd6d93a6825054ac~mv2.png", "Figure 15") + cap("Figure 15. Linear vs. nonlinear: GLM vs. XGBoost")
      + "<p>Although the preliminary analysis using supervised learning offered some insights into the dataset, these models did not fulfill our goal of recommending the next few books to our target users. Moreover, to run the models, we eliminated a few variables because of the constraints that certain models placed on data types. This procedure improved the efficiency of training and building the models, but we may also have lost useful information in the process.</p>"
      "<h3>Unsupervised Learning: Cluster Analysis</h3>"
      "<p>The purpose of our app was to filter and recommend books to users. One of the state-of-the-art practices in building recommendation filtering systems is to use collaborative filtering algorithms, which are often considered clustering algorithms. Additionally, unsupervised learning outperformed supervised learning in finding potential patterns across different types of data.</p>"
      "<p>The ‘clValid’ package in R was used to carry out clustering on the dataset. Intuitively, the following parameters are the most relevant to users when recommending the best books: average rating, genre, format, and book length (number of pages). These features were incorporated into our analysis after preprocessing, which included binary encoding of categorical variables, scaling of the data points, and removal of NA or missing values.</p>"
      "<p>We concluded that K-means clustering would suit our dataset better than hierarchical clustering for two main reasons. First, our dataset was large, and binary encoding would increase the number of variables that the algorithm had to handle. Second, K-means allows more flexibility across clusters because a data point can be reassigned to another cluster.</p>"
      "<p>Using the clValid package, we obtained a cluster plot with the ‘kmeans’ method for 11 clusters. We validated 11 as the optimal number of clusters using silhouette and stability validation methods across a range of 2 to 11. The highest silhouette score was associated with 11 clusters, as shown in the fviz_nbclust plot below.</p>"
      + dimg_m("book_f16", "f4a835_2383c48218274974a2e60a8192b80d91~mv2.png", "Figure 16") + cap("Figure 16. The silhouette method for the optimal number of clusters")
      + dimg_m("book_f17", "f4a835_4d6188ee5d574fe19040a55232957a85~mv2.png", "Figure 17") + cap("Figure 17. Cluster plot")
      + "<p>The resulting clusters are very close to and overlap with one another. Dimensionality-reduction methods such as UMAP and PCA can help resolve this issue. The UMAP function was used on our dataset to reduce it to two dimensions and produce cleaner, tighter clusters.</p>"
      + dimg_m("book_f18", "f4a835_0adf70bc5bf344f08a13fd1857c94758~mv2.png", "Figure 18") + cap("Figure 18. K-means clustering based on UMAP-transformed data")
      + "<p>The green points in the plot appear to be outliers, but they are actually a cluster of 10 points. A deeper analysis revealed that they belonged to the “Audio CD” format, with lengths ranging from 0 to 10 pages. This seems peculiar because audiobooks should not intuitively have ‘pages’ associated with them.</p>"
      "<p>The ‘kmeans’ function in R can also be used to fit the data. It is less complex and does not offer the same functionality as clValid, but with a little analysis, it allows for greater interpretability of the different characteristics within each cluster. Here, the kmeans function was used with 11 clusters, and the data was filtered to obtain data points belonging to cluster 2: books in the ‘Children's Books’ genre and ‘Board Book’ format.</p>"
      + dimg_m("book_f19", "f4a835_f2dc078b0e0842ff8ea781b6918cd4bd~mv2.png", "Figure 19") + cap("Figure 19. K-means clustering using the ‘kmeans’ function")
      + "<h3>Collaborative Filtering</h3>"
      "<p>Nevertheless, it would not be easy for our app to rank all the books within the same cluster, so the accuracy of the model might be compromised. In addition, both models used dimensionality-reduction methods, which reduce their interpretability for the audience. A few algorithms have proved effective, and Riesterer et al. (2020) examined how noise levels affect the performance of each algorithm. As they suggested, UBCF and IBCF outperformed MFA in a noisier dataset environment. In our app, the algorithm code contributed through Kaggle includes both UBCF and IBCF algorithms. However, it would be helpful to conduct heuristic evaluations with our users to better understand their experience.</p>"
      + dimg_m("book_f20", "f4a835_1e8bbd09d7794f2dbc87a56bcd54cdf7~mv2.png", "Figure 20") + cap("Figure 20. Performance graph: UBCF vs. IBCF vs. MFA")
      + "<h3>Text Analysis: TF-IDF Word Cloud</h3>"
      "<p>Data: book descriptions. Features: captures some information and runs quickly. Challenges: different languages and a small dataset.</p>"
      + dimg_m("book_f21", "f4a835_5359bb5dd98a4f8eba8834d29fbe59da~mv2.png", "Figure 21") + cap("Figure 21. Word cloud example")),
     ("Application and Conclusions",
      "<h3>Basic Prototype</h3>"
      "<p>First, we came up with a simple prototype consisting of three parts. In the first column, people can choose genres and rate books they like. In the second column, they can filter recommendations. Finally, they can see the recommended books. Using the arrow button, users can view more recommendations. Word clouds are created from each book's description and help users quickly understand what the recommended book is about.</p>"
      + dimg_m("book_f22", "f4a835_0426658c134c4209a9eba4361559c9dc~mv2.png", "Figure 22") + cap("Figure 22. Basic prototype")
      + "<h3>Demonstration Application</h3>"
      "<p>Based on the R Shiny example on Kaggle, we developed two new features: genre selection filtering and a word cloud for recommended books. Because we used a different dataset consisting of children's books and fantasy books, we made recommendations based on the user's genre selection. After users receive a recommendation, they can view the word clouds and understand the unique features of the recommended books. You can find the test version here: <a href='https://edaxplor.shinyapps.io/book_v4/' target='_blank' rel='noopener'>edaxplor.shinyapps.io/book_v4</a>.</p>"
      "<h3>Conclusion</h3>"
      "<p>The demo showed that UBCF works well for book recommendations. However, we think the prototype can be improved further by strengthening trust and persuasion. These are areas for future improvement. Conducting user testing would also be an effective way to evaluate our service.</p>"
      "<ul><li>We used a username and bookshelf as a title to create a sense of personalized service.</li>"
      "<li>We separated the user's bookshelf into two parts: a ‘Reading Now’ shelf and a ‘To Read’ shelf. By doing so, the algorithm can understand the user's current and future interests.</li>"
      "<li>By showing other users' bookshelves, we wanted to give users the feeling that the website is a book-reading community. We think we can also add curated book sections to support augmented AI-human collaboration.</li>"
      "<li>Users can like or dislike a recommendation. Based on this feedback, the algorithm can reflect the user's preferences and apply them to future recommendations.</li></ul>"
      + dimg_m("book_f24", "f4a835_493bf1119f444dc78bce71f3d0806895~mv2.png", "Figure 24") + cap("Figure 24. Detailed prototype for future development")),
     ("References",
      "<ul>"
      "<li>Genre Dataset: <a href='https://sites.google.com/eng.ucsd.edu/ucsdbookgraph/home' target='_blank' rel='noopener'>UCSD Book Graph</a></li>"
      "<li>Mengting Wan, Julian McAuley, “Item Recommendation on Monotonic Behavior Chains”, RecSys'18.</li>"
      "<li>Mengting Wan, Rishabh Misra, Ndapa Nakashole, Julian McAuley, “Fine-Grained Spoiler Detection from Large-Scale Review Corpora”, ACL'19.</li>"
      "<li>Rating Dataset and Recommendation Algorithms: <a href='https://www.kaggle.com/philippsp/book-recommender-collaborative-filtering-shiny/code' target='_blank' rel='noopener'>Kaggle: Book Recommender (Collaborative Filtering, Shiny)</a></li>"
      "<li>Riesterer, N., Brand, D., &amp; Ragni, M. (2020). Uncovering the Data-Related Limits of Human Reasoning Research: An Analysis based on Recommender Systems. arXiv:2003.05196.</li>"
      "<li><a href='https://towardsdatascience.com/10-tips-for-choosing-the-optimal-number-of-clusters-277e93d72d92' target='_blank' rel='noopener'>Choosing an optimal number of clusters</a></li>"
      "<li><a href='https://towardsdatascience.com/how-exactly-umap-works-13e3040e1668' target='_blank' rel='noopener'>Working and benefits of UMAP</a></li>"
      "</ul>")], back="ux-projects.html",
    hero=hero_img("book_hero", "f4a835_ddc7400150214afebb07f52a82c092f8~mv2.png", "Book Recommendation System"))

detail("lexiainwonderland.html", "Lexia in Wonderland", "UX Projects",
    [("Keywords", "Multisensory Instruction, Gamification, UX research"),
     ("Members", "Daye Kang, Hye-Ryeong Kim, Ji-Hae Lee"),
     ("My contribution", "Team Leader, UX research, Prototyping, Illustration"),
     ("Year", "2017")],
    "<p>‘Lexia in Wonderland’ is a game that uses letter blocks to create nonwords and is designed specifically to help dyslexic children learn phonics.</p>",
    [("What inspired this project",
      split(dimg_s("lex_inspire", "f4a835_49f52abf9825426989ceb479db4ac6d1~mv2.jpg", "Like Stars on Earth")
            + cap("The film explores the life and imagination of Ishaan, an 8-year-old dyslexic child. Although he excels in art, his poor academic performance leads his parents to send him to a boarding school. Ishaan's new art teacher suspects that he is dyslexic and helps him to overcome his disability. (From Wikipedia)"),
            "<p>I became aware of dyslexia after watching the movie ‘Like Stars on Earth’ (2007), which is about a dyslexic child and an art teacher who understands his difficulty and helps him learn to read. After researching how dyslexia is treated in Korea, I found that there was almost no research on or understanding of dyslexia. There was also no digital service specifically designed to help dyslexic children practice Korean at home. About 330,000 children in Korea have dyslexia. Even though they have potential, they are neglected by the current education system, which focuses on reading. Through my work, I wanted to help dyslexic children and increase awareness of dyslexia.</p>")),
     ("Background",
      "<p>Around 5 to 10 percent of children worldwide have dyslexia. Of the 50 million people in Korea, 5 million have dyslexia.</p>"
      + dimg_m("lex_bg_1", "f4a835_a2a94f51d5fb47f6849d32017415c6dc~mv2.png", "Dyslexia statistics")
      + "<p>The Korean language has its own writing and pronunciation systems. Korean characters are called Hangeul, and their shapes are based on the shape of the mouth when making sounds.</p>"
      + dimg_m("lex_bg_2", "f4a835_aad66f0b680b4b8bb88c4472999ea80e~mv2.png", "Hangeul")),
     ("Problems",
      "<ul>"
      "<li><b>Missed Opportunity</b>: There is a crucial timeframe for treating dyslexia. Once this window is missed, the symptoms get worse.</li>"
      "<li><b>Low Self-Esteem</b>: Dyslexia can cause low self-esteem and other mental health problems in a school environment that focuses on reading. Dyslexic children are often mocked by their peers.</li>"
      "<li><b>Expensive Treatment</b>: Treatment is too expensive, and most people waste money on unproven methods.</li>"
      "<li><b>No Guidance for Parents</b>: Parents have a hard time teaching and providing guidance to their dyslexic children.</li>"
      "</ul>"
      + "<p>In Korea, awareness and understanding of dyslexia are limited compared with other countries. It is essential to treat dyslexia before children reach the age of 8, yet many children go through life undiagnosed. Parents also have a hard time guiding dyslexic children, and there are few materials that explain dyslexia treatment to them.</p>"
      + dimg_m("lex_prob", "f4a835_5b9689bfdaf94cf09514444e7d2ee18b~mv2.png", "Problems")),
     ("About Dyslexia",
      "<h3>What Is Dyslexia?</h3><p>Dyslexia is a reading disorder characterized by difficulty reading accurately and fluently, as well as difficulty with spelling. Reading is a big part of the Korean curriculum. If children fail to overcome dyslexia at an early age, they can be bullied at school, leading to low self-esteem. The trauma from childhood can affect them well into adulthood.</p>"
      + dimg_m("lex_dys_1", "f4a835_0dd5ef465aff4ae893cc408f9adf9ea6~mv2.jpg", "About dyslexia")
      + "<h3>Symptoms</h3><p>Symptoms are often first noticed by a teacher or parent when children are around 8 or 9 years old. Teachers and parents can recognize the signs when children's academic performance falls behind that of their peers. By ages 9 or 10, children may have difficulty reading one-syllable words or understanding phonology. They have difficulty understanding the order of consonants and vowels. By age 12, they often make spelling mistakes and show poor writing ability. They also have difficulty memorizing dates, people's names, and numbers. Even in adulthood, they may still have difficulty reading and continue to make spelling mistakes.</p>"
      + "<h3>Is Dyslexia Curable?</h3><p>Yes. In the past, people thought dyslexia was caused by visual impairments. However, research in cognitive psychology has shown that dyslexia is a neurological disorder in the left hemisphere of the brain. The left hemisphere of a person with dyslexia cannot store text and sounds or combine them quickly. If dyslexia is diagnosed after age 10, it is much harder to treat. Younger brains are more flexible and more likely to form neural circuits properly. Therefore, early detection is critical. Once children miss this timeframe, they must make greater efforts to keep up with their peers.</p>"
      + dimg_m("lex_dys_2", "f4a835_97a4f4cd6b8a4a5d828f560524bada26~mv2.jpg", "Brain and dyslexia")
      + "<h3>How to Treat Dyslexia: What Are the Problems with Current Methods?</h3><p>Phonology should be taught by linking written forms to sounds. However, there are problems with current education methods.</p>"
      "<ul><li>Books currently used in medical institutions and homes to treat dyslexic children are often difficult to understand. As a result, children lose interest in learning Hangeul (Korean characters) and often refuse to take classes.</li>"
      "<li>It is difficult to keep up with expensive private classes that cost more than $100 per hour.</li>"
      "<li>There is a lack of medical centers that specialize in treating dyslexia. These centers are often far from where dyslexic children live. Sometimes, parents fly from Jeju Island to visit a medical center in Seoul.</li></ul>"
      + dimg_m("lex_dys_3", "f4a835_0980b031eb004eb3bcc376372c82b806~mv2.jpg", "Current treatment"),
      "banded band-purple dk"),
     ("Research Process",
      "<h3>User Interview</h3><p>We interviewed groups of nonexperts and experts. The picture below shows an interview with a college student named A, who had a difficult school life because of dyslexia.</p>"
      + dimg_m("lex_rp_interview", "f4a835_611b2f5a21b547c991f05f58321f2c83~mv2.png", "User interview")
      + '''<div class="int-grid">
      <div class="int-col"><h3>Non-Experts</h3>'''
      + int_card(dimg_s("lex_rp_p1", "f4a835_33326f8456604575874731eef18dd563~mv2.jpg", "Interviewee A"),
                 "01.", "A", "University student with dyslexia / 24 years old",
                 "“I wish I had learned about my dyslexia earlier, too. Now that I'm an adult, there's not much I can do to ease the symptoms.”",
                 "“I had a hard school life. I failed the university entrance exam several times, and after I got in, I had to record every class and all my textbooks because I had difficulty reading.”")
      + int_card(dimg_s("lex_rp_p3", "f4a835_f54f428b28ce487c8f474b6db2c4a98c~mv2.jpg", "Mrs. B"),
                 "02.", "Mrs. B", "Homemaker raising a dyslexic child / 38 years old",
                 "“After several months of receiving treatment at the institution, I stopped because it was too far away and expensive. I'm trying to teach at home, but it's not easy.”",
                 "“I give my son homework, but he runs away. The therapist said the homework is only useful if he practices every day.”")
      + '''</div>
      <div class="int-col"><h3>Experts</h3>'''
      + int_card(dimg_s("lex_rp_p2", "f4a835_52278f31ed6b42f0ace539f62c35a37b~mv2.jpg", "Hyun-Ji Um"),
                 "03.", "Hyun-Ji Um", "Language therapist / 42 years old",
                 "“Children have different levels of dyslexia, so they need a customized education.”",
                 "“To adjust well to school life, it is better to start treatment before the child starts school.”",
                 "“Children who study with me attend classes once or twice a week. However, it is essential to practice Korean every day, even when they don't visit the medical center for class.”")
      + int_card(dimg_s("lex_rp_p4", "f4a835_2ac8c04cd2d7451e91caac9a7d36ecbf~mv2.jpg", "Jae-Seok Jung"),
                 "04.", "Jae-Seok Jung", "Dyslexia expert / 46 years old",
                 "“No matter how hard you try after the third grade of elementary school, you cannot achieve the same fluency as the average person.”")
      + "</div></div>"
      + "<h3>Affinity Diagram</h3><p>We wrote down keywords from the interviews and then rearranged them into categories.</p>"
      + row("", dimg_s("lex_rp_aff1", "f4a835_1a09008244bb4cefa9f9cc5ef7afd1d8~mv2.png", "Affinity diagram"),
               dimg_s("lex_rp_aff2", "f4a835_2c569d494bd74ed9a996280fcdce1c11~mv2.png", "Affinity diagram categories"))
      + "<h3>Persona 1: Min-Jung Kim / 38 years old</h3>"
      + split(dimg_s("lex_rp_per1", "f4a835_c200023dcb55453384c6c77b0b3f4899~mv2.png", "Persona 1"),
        "<p><b>Situation:</b> She is a working mom who raises a dyslexic child. <b>Thinking:</b> She wants to spark her child's interest in reading and practice Korean with him every day.</p>"
        "<p><b>Conditions:</b> Min-Jung Kim is an office worker who has an eight-year-old son. He has difficulty reading or writing Korean compared with other children his age. She suspected that he had dyslexia and enrolled him in a special class at an institution once a week. As time went by, she felt burdened by the high tuition and the distance to the medical center. Her son was also not very interested in learning Korean. Eventually, she gave up on the treatment, and now she plans to buy dyslexia education books and teach Korean to her son. However, her son tries to run away. To teach him in person, Min-Jung also has to study Korean phonics so she can teach her son effectively. However, she feels frustrated because she does not have enough time to spare.</p>"
        "<p><b>Needs:</b> 1) I want to diagnose my child at home if he is suspected of having dyslexia. 2) I want to treat dyslexia anywhere and at a low cost. 3) I hope there is an engaging educational service that can interest my child. 4) I want to teach Korean as frequently as possible. 5) I want to see my child's progress.</p>")
      + "<h3>Persona 2: Jee-Hee Park / 8 years old</h3>"
      + split(dimg_s("lex_rp_per2", "f4a835_54acbd64a7184d91bc99dc8e2c98257d~mv2.png", "Persona 2"),
        "<p><b>Situation:</b> He has low self-esteem because of his poor reading skills. <b>Thinking:</b> He wants to read as well as his friends and wants others to understand his difficulties.</p>"
        "<p><b>Conditions:</b> He feels left behind because his peers are good at reading, but he isn't. He wants to avoid reading in front of the class. He is often seen as problematic and lazy, even though poor reading is only a symptom of dyslexia that he cannot control. He gets angry because his parents treat him like a problem child because he cannot read. This misunderstanding causes trouble within the family. In classes with a language therapist who specializes in dyslexia, he enjoys learning Korean, even when it is difficult, because the therapist guides him well. However, when he is learning Korean at home with his parents, he becomes less interested because his parents are not as good as the therapist at guiding him. This worsens the relationship between the child and his parents. Instead of learning Korean, he wants to play games all day. Because he hates reading, his confidence has decreased and his grades have dropped.</p>"
        "<p><b>Needs:</b> 1) I want learning Korean to feel like a fun game. 2) I want to read as well as my friends. 3) I don't want to fight with my parents. 4) I want others to understand my difficulties.</p>")
      + "<h3>Experience Mapping: Parents' Point of View</h3>"
      "<p><b>Discover:</b> Parents start to recognize that their children are falling behind their peers. If parents do not observe them carefully at this stage, they may not take the symptoms seriously and may miss the treatment window. Parents may confuse dyslexia with other conditions, such as ADHD or other learning difficulties. There is a risk of pursuing non-scientific practices such as oriental medicine or eye training to improve reading ability.</p>"
      "<p><b>Treatment:</b> A specialist confirms that the patient has dyslexia. The child starts a dyslexia therapy program, visits once or twice a week, and works with language therapists. Therapists often give homework to encourage steady learning; however, the homework is often left undone. The symptoms may begin to improve.</p>"
      "<p><b>Giving Up:</b> Parents try to teach Korean to the child at home. The child refuses to learn because the parents are not teachers. Since parents are not experts, it is hard to teach children without proper guidelines.</p>"
      "<p><b>Solution Points:</b> If users suspect dyslexia, they can use the Diagnostic function in the app to receive guidance on whether to visit a specialized institution for a diagnosis. With the application, children can continue learning Korean at their own pace when they are not attending classes at the institution. Exciting content in the app encourages children to study with their parents without a teacher. The application also provides parents with guidance on how to support their children. If the parents are too busy to teach, children can study by themselves.</p>"
      + dimg("lex_rp_map", "f4a835_aa82a04e5259416fa05a99aa18f0bd94~mv2.jpg", "Experience mapping")),
     ("Design Insights",
      quote("“An engaging service that helps dyslexic children study Korean at home and practice consistently”")
      + "<h3>Service Overview</h3><p><b>Who:</b> Dyslexic children from 5 to 10 years old<br><b>What:</b> Korean phonics practice using nonwords<br><b>When:</b> Every day at home when they do not visit the specialist institution<br><b>How:</b> Actively and continuously, by themselves or with parents</p>"
      + "<h3>Concept</h3><p>We combined content from the book ‘Reading Confidence’ with the story of ‘Alice in Wonderland’ to provide more engaging learning experiences. We saw similarities between dyslexic children experiencing strange letters and Alice meeting unusual characters in Wonderland. We therefore applied the story of Alice in Wonderland to our app design. We transformed the books into digital multimedia content. Children can use multimedia content on their digital devices to practice Korean. After imitating the mouth shape, children can record themselves and compare their movements with the correct answer.</p>"
      + dimg_m("lex_di_1", "f4a835_7040de464d1644c88605e231d9551e1e~mv2.jpg", "Concept")
      + '<div class="compose reveal">'
      + f'<img class="bg" src="{A("lex_di_4", "f4a835_1f57981bd48046c6bb28dd832a21f614~mv2.png", "fit", 900, 1400)}" alt="Reading Confidence and Alice in Wonderland books">'
      + f'<img class="char-l" src="{A("lex_di_3", "f4a835_57300d50f13c428fbd13ddf95059548a~mv2.jpg", "fit", 500, 700)}" alt="Character">'
      + f'<img class="char-r" src="{A("lex_di_2", "f4a835_aa4ce85b381740ea8676dd3022ccbefb~mv2.jpg", "fit", 500, 700)}" alt="Alice character">'
      + '<span class="arr">&#8594;</span></div>'
      + cap("Combining the book ‘Reading Confidence’ with the story of ‘Alice in Wonderland’")
      + "<h3>Design Ideas</h3><p>To maintain the benefits of professional dyslexia treatment and maximize the benefits of online and digital content, we embraced the following methods: Multisensory Instruction, Storytelling, Personalized Instruction, and Gamification.</p>"
      + "<h3>1. Multisensory Instruction</h3><p>We decided to use multisensory instruction to enable children to learn Hangeul by using various senses such as sound and touch.</p>"
      + "<h3>2. Storytelling</h3><p>Alice meets the characters who represent each chapter and travels through each stage to return to reality. The structure follows a ‘growth epic’. We created a fantasy setting for the game to stimulate children's imaginations. Fun and friendly characters help children learn Hangeul and overcome emotional trauma.</p>"
      + arrow_row(dimg_s("lex_di_5", "f4a835_7921e168ae544528acd1b036179795f1~mv2.png", "Storytelling"),
                  dimg_s("lex_di_6", "f4a835_77fb3212967a43a4a4fe7ff5caed23c5~mv2.png", "Story structure"))
      + dimg_m("lex_di_7", "f4a835_817d659b03f2432a8d5325492827699f~mv2.jpg", "Characters")
      + "<h3>3. Personalized Instruction</h3><p>The application provides guidance through learning steps based on each child's needs. Children can focus on improving their weaker areas by checking them on the ‘report’.</p>"
      + dimg_m("lex_di_8", "f4a835_beddd716fc1a4a2e960c20fa9a9103f4~mv2.png", "Personalized instruction")
      + "<h3>4. Gamification</h3><p>On ‘My page’, children can see their progress. Gamification of the learning process can help children become interested in learning Korean. The application gives positive feedback and encouragement while children play the game. It encourages them to continue learning Korean voluntarily. The application uses a reward system. Children earn badges whenever they make progress.</p>"
      + row("",
            dimg_s("lex_di_9", "f4a835_af9ecb2d15be4fe1904c4da288d9c2ea~mv2.png", "Gamification"),
            dimg_s("lex_di_10", "f4a835_cec181c1bfe04f71b2b885cd90f13565~mv2.jpg", "My page"),
            dimg_s("lex_di_11", "f4a835_785071bcf0fe4819a5f08b5c2aee95d0~mv2.png", "Rewards"),
            dimg_s("lex_di_12", "f4a835_a521d54905244777a93e879594c4d491~mv2.png", "Badges")),
      "banded band-lav"),
     ("Low-fi Prototype",
      "<h3>Diagnosis</h3><p>The app diagnoses dyslexia by assessing how well children understand the principles of consonants and vowels. Based on the results, it assesses their level of fluency. The app plays instructions that guide children to replace consonants or vowels based on what they heard (for example, which vowel they need to change ‘Nack’ to ‘Nock’). The app asks children to record their voices while reading the text in the box within a set amount of time. It measures how fluently they read the text.</p>"
      + "<h3>Learning Phonics</h3><p>Using multimedia content, children learn how to pronounce letters. The app shows mouth movements and how the tongue is positioned within the mouth to teach children how to pronounce each consonant and vowel.</p>"
      + "<h3>Phonics Game</h3><p>Based on the phonics that children have learned, they play a phonics game. Children listen to the pronunciation of vowels and then select the answers in order.</p>"
      + "<h3>Understanding Phonemes</h3><p>Children learn how phonemes are pronounced when they are next to each other. When children combine specific phoneme blocks, the app shows how adjacent phonemes are pronounced.</p>"
      + "<h3>Report</h3><p>They receive a report based on their play session. The child and their parents can view the child's progress in visual graphs, and the report provides guidance to the parents. The report page shows children and parents how much they are improving, identifies common mistakes, and provides feedback.</p>"
      + row("",
            dimg_s("lex_lp_1", "f4a835_bcdf7c3a133b429ab72d3311f0204fe5~mv2.png", "Low-fi prototype: diagnosis"),
            dimg_s("lex_lp_2", "f4a835_f32a16c211a641c88cad91a53b9c4ca6~mv2.png", "Low-fi prototype: fluency test"),
            dimg_s("lex_lp_5", "f4a835_bd1ea775526b45f3b5629f89f285046e~mv2.png", "Low-fi prototype: learning phonics"),
            dimg_s("lex_lp_6", "f4a835_022e1a6142a74eb2870770c733c8d960~mv2.png", "Low-fi prototype: phonics game"),
            dimg_s("lex_lp_3", "f4a835_b0070ac240f345e3b2d12f6aad213572~mv2.png", "Low-fi prototype: understanding phonemes"),
            dimg_s("lex_lp_4", "f4a835_cef788a0ef63439da4864b0aa92ab370~mv2.png", "Low-fi prototype: report")),
      "banded band-dark dk"),
     ("Test & Development",
      "<h3>Wizard of Oz Testing with a Dyslexic Child and Her Caregiver</h3>"
      "<p>We tested the prototype with an 8-year-old dyslexic child, ‘Ji-Yoon’. First, we asked the father to teach the child how to pronounce certain vowels using the textbook used in offline lessons. Then, we asked Ji-Yoon to learn other vowels using the application. We received qualitative feedback from both the father and Ji-Yoon indicating that the application made learning Korean phonics more fun. The father mentioned that it reduced the burden of teaching phonics to the child and that the application served as a guide for him.</p>"
      + row("", dimg_s("lex_td_1", "f4a835_ab8da5cc217b49afa6859013272246a9~mv2.png", "Learning pronunciation with the parent using a book"),
               dimg_s("lex_td_2", "f4a835_7fc85f8ee74341cf8fe37f0312b2a2b9~mv2.png", "Ji-Yoon using the application on her own"))
      + cap("Left: learning pronunciation with the parent using a book · Right: Ji-Yoon is using the application instead of the book to learn Korean vowels on her own")
      + "<h3>Expert Interview</h3>"
      + quote("“Instead of regular words, dyslexic children should practice non-words”<br>Dr. Jae-Seok Jung, dyslexia expert and author of ‘Reading Confidence’")
      + "<p>Even though we received positive feedback from the dyslexic child and the caregiver, we wanted feedback from an expert. We interviewed Dr. Jae-Seok Jung, a dyslexia expert who wrote ‘Reading Confidence’ for dyslexic children. It is the only book in Korea designed especially for dyslexic children. Because our application is based on the book's content, we thought it was natural to ask for his opinion on the application design. He emphasized the importance of practicing ‘non-words’ because dyslexic children tend to memorize whole words instead of understanding phonics. Therefore, it is essential for children to practice phonics with non-words. This practice helps them read new words naturally when they encounter them.</p>"
      + dimg_m("lex_td_3", "f4a835_ee8297b2acdd4c1e9f986ee72685e06e~mv2.jpg", "Expert interview with Dr. Jae-Seok Jung")
      + "<p><b>What are non-words?</b> A non-word is a combination of letters that has no meaning. Regular words: Cat, Museum. Non-words: Caet, Mooseum.</p>"
      "<ul><li>“We need to teach them in the form of individual characters, unlike the usual Hangeul education apps that are currently available on the market.”</li>"
      "<li>“We definitely need games for dyslexic children to help them enjoy learning Korean at home.”</li>"
      "<li>“Instead of trying to put all the content from the book into the app, I believe it is better to focus on repetitive training.”</li></ul>"
      + "<h3>Developing the Prototype for the Non-words Block Game</h3>"
      "<p>Based on the expert interview, we decided to develop the app further by creating a multi-sensory game that enables children to use word blocks to combine words. This idea came from previous studies suggesting that block play improves reading skills.¹ After hearing non-words pronounced, the user creates them using letter blocks. The webcam then records the activity and sends data to the computer. We used the software ‘Processing’ and image recognition to provide feedback on whether the answer is correct.</p>"
      + cap("1. Effect of Block Play on Language Acquisition and Attention in Toddlers. Dimitri A. Christakis, MD, MPH; Frederick J. Zimmerman, PhD; Michelle M. Garrison, PhD. American Medical Association")
      + row("", dimg_s("lex_td_4", "f4a835_9b0e6fad09644b66a85536c6ac94deaf~mv2.png", "Block game prototype"),
               dimg_s("lex_td_5", "f4a835_15681312efbc4d1a8d6783c3decb9bab~mv2.gif", "Block game demo"))
      + "<h3>The flow of the block game</h3>"
      + flow_center("Start",
            dimg_s("lex_td_6", "f4a835_07ce20bcd25e4d1bab0dd82db53d3fb4~mv2.gif", "Block game: start"),
            "The caterpillar reads non-words and asks the child to combine letter blocks to make what they heard.")
      + row("",
            lcol("Wrong",
                 dimg_s("lex_td_7", "f4a835_d28047b5811746889f4b43fcdba897fe~mv2.png", "Block game: wrong answer"),
                 dimg_s("lex_td_9", "f4a835_02add8cb632c4787bc91c22539311bfa~mv2.gif", "Wrong feedback"),
                 cap("The caterpillar tells the user that the answer is incorrect and encourages them to retry.")),
            lcol("Correct",
                 dimg_s("lex_td_8", "f4a835_367787460a2347e7860eb0dae6701eda~mv2.png", "Block game: correct answer"),
                 dimg_s("lex_td_10", "f4a835_58d938cc05b44203b0e76b9e90a6b56f~mv2.gif", "Correct feedback"),
                 cap("The caterpillar tells the user that the answer is correct and offers verbal praise to keep them motivated."))),
      "banded band-gray"),
     ("Final Design",
      sub_band("band-plum dk", "<h3>Mood Board</h3>", dimg_m("lex_fd_mood", "f4a835_90e864729a22429db380007d68f0cd16~mv2.png", "Mood board"))
      + "<h3>UI Design</h3>"
      + dimg("lex_fd_ui1", "f4a835_0fee4deceb8647ec89b85b121fbf3779~mv2.jpg", "UI design")
      + dimg_m("lex_fd_ui2", "f4a835_c56600119746473ba028772ca795964d~mv2.jpg", "UI design screens")
      + dimg_m("lex_fd_ui3", "f4a835_19619498ec1448248541516b7679a67b~mv2.png", "UI design screens")
      + dimg_m("lex_fd_ui4", "f4a835_b7791e56b7d6485e9c0ab96a193cca3d~mv2.png", "UI design screens")),
     ("Exhibition",
      '<div class="lexia-exhibition-grid">'
      + dimg_s("lex_ex_1", "f4a835_dec4e1565bf442ddaaff286bc7f05f33~mv2.png", "Lexia in Wonderland exhibition installation")
      + dimg_s("lex_ex_2", "f4a835_e96674a0c066468cb8f42ffb0723cf75~mv2.png", "Visitor viewing the Lexia in Wonderland exhibition")
      + '</div><div class="lexia-exhibition-detail">'
      + dimg_s("lex_ex_3", "f4a835_d8b5d10daa84464794a61f76461e7978~mv2.jpg", "Hangeul letter blocks at the exhibition") + "</div>",
      "banded band-gray")],
    awards="2017 Adobe Design Achievement Awards&nbsp;Semifinalist · 2017 KSDS Excellence Award · 2017 Hongik University Excellence Graduation&nbsp;Work",
    hero=hero_img("lex_hero", "f4a835_f2337819babf4271ad20dca7ad430aa5~mv2.png", "Lexia in Wonderland"))

detail("nudgedesign.html", "Nudge Design to Increase Physical Activities of Hospitalized Children", "UX Projects",
    [("Keywords", "Nudge Design, Gamification, UX research, Hospitalized children"),
     ("Members", "3"),
     ("My contribution", "Team Leader, UX research, Prototyping, Illustration"),
     ("Year", "4.2017 – 11.2017")],
    "<p>Footprints nudge children to walk, and their various shapes encourage children to stretch their legs. The story-based wallpaper makes walking more engaging. Children can stretch their necks or arms by following the movements of the animals on the wallpaper.</p>",
    [("What inspired this project",
      "<p>I became more interested in problems in children's hospitals while designing a family communication service for children who were hospitalized long term. During the interviews, our team found that a lack of physical activity and play in children's hospitals was a problem. This project was funded by the Samsung Tomorrow Solution.</p>"),
     ("Service Summary",
      "<p><b>Reality:</b> Lack of physical activity can cause stress and slow recovery for hospitalized children. However, even though children want to walk, there are no suitable trails that they can enjoy every day.</p>"
      "<p><b>Problem:</b> Currently, children can use outdoor trails or an indoor hallway for walking. The outdoor trails are easily affected by the weather. Fine dust also prevents children from using them as often as needed. The indoor hallway is dull and boring, so the children do not enjoy walking there. Because a lack of physical activity can slow recovery and cause stress, it is important to ensure that children can take a walk every day.</p>"
      "<p><b>Solution:</b> By providing a safe and fun trail design, we can help children relieve stress from the daily treatment process. Considering the hospital's budget constraints, we created a nudge design in the hallway to make walking more engaging. Characters and stories on the wall can motivate hospitalized children to take walks every day.</p>"
      + quote("“Why are there no children playing at a children's hospital?”")
      + "<p><b>Importance:</b> This solution can provide a positive hospital experience for children, and it can help them recover more quickly.</p>"
      + dimg_m("nud_ss_1", "f4a835_907981ea09424f9c99626f1513ed2d0a~mv2.png", "Service summary")),
     ("Research Process",
      "<h3>Desk Research: Online Research</h3><p>We observed posts on social networks such as Instagram, blogs, and internet cafes to understand physical activity and entertainment in children's hospitals.</p>"
      "<p><b>Daily life spent in bed all day:</b> The hospital is a shared space, so people avoid letting their children play noisy games. A guardian may give a child a smartphone because the child likes watching videos with a headset, and it is relatively quiet. Due to concerns about spreading infections, it is not easy to meet friends in the hospital.</p>"
      + row("", dimg_s("nud_rp_1", "f4a835_02fd4f2675fb4193a500ecbbf5f593cf~mv2.png", "Desk research"),
               dimg_s("nud_rp_2", "f4a835_2d0bac393cbd4cf7adb74f25bb1a3077~mv2.png", "Online research"))
      + "<h3>Field Research: A Quantitative Survey of Hospital Movements</h3>"
      "<p>We surveyed thirty-two children for four days, and the survey showed that they moved for no more than 20 minutes in the hospital. According to the paper, children need to walk 12,000–15,000 steps for their physical health, but the hospitalized children did not take more than 2,000 steps.</p>"
      + cap("* About 110 steps per minute for a walk, 140 steps for a fast walk, and 180 steps for jogging.")
      + row("", dimg_s("nud_rp_3", "f4a835_7c99abb74eb34d1c9eb40c19d4242657~mv2.png", "Survey"),
               dimg_s("nud_rp_4", "f4a835_55edc73b636140d593fc5e3848f1f758~mv2.png", "Survey results"))
      + "<h3>Observation</h3><p>We visited children's hospitals, including Asan Medical Center, Severance Hospital, and Seoul National University Hospital, where we observed and interviewed nurses and hospitalized children.</p>"
      + row("", dimg_s("nud_rp_5", "f4a835_0cda220471a34ddea90747c114712632~mv2.png", "Outdoor trails"),
               stack(dimg_s("nud_rp_8", "f4a835_0bccf00b736041ed80c211a61733f6b6~mv2.png", "Indoor installation"),
                     dimg_s("nud_rp_6", "f4a835_9e026236e3604d78a9131cded541bed3~mv2.png", "Indoor installation 2")))
      + split(dimg_s("nud_rp_7", "f4a835_6630b0be9bcf4978b9b4f7c8dd966d02~mv2.jpg", "Hey-Jin Kim"),
              qa("Hey-Jin Kim, 10 years old · Seoul National University Children's Hospital",
                 "When we found that she was not bringing all of her things from the refrigerator to her bed at once, we asked her why.",
                 "“I intentionally do not bring all the food that I need at once because it forces me to walk more. My doctor always says I have to work out when I'm in the hospital.”"))
      + "<h3>Field Research: Asan Design Innovation Center</h3>"
      "<p>We interviewed staff at the Asan Medical Design Innovation Center about children's physical activities. Asan Children's Hospital had no play space for children, and there was little awareness of their physical activity. Regarding children's physical activity, a nurse mentioned that walking was enough: “Since children cannot exercise vigorously in a hospital, walking can be enough.”</p>"
      + quote("“Walking is a great exercise for hospitalized children.”")
      + row("c21", dimg_s("nud_rp_9", "f4a835_6c0f084f18bb484bafccfc6d981b1a92~mv2.png", "Asan Design Innovation Center interview"),
                   dimg_s("nud_rp_10b", "f4a835_88e8604a9e354495ba5c44fd0b2ab260~mv2.png", "A nurse working at the children's hospital"))
      + "<h3>Affinity Diagram</h3><p>Based on the affinity diagram, we developed three insights from the stakeholders' viewpoints.</p>"
      "<p><b>Hospitalized children:</b> They cannot move easily because of IV poles. The space does not feel like a play area because of adult control.</p>"
      "<p><b>Parents:</b> When children play in the hallway, it is easy to observe their activities and seek medical attention in case of a problem. However, parents were concerned about obstructing the hallway for other patients and clinicians.</p>"
      "<p><b>Hospital:</b> The hallway is suitable for walking because it does not require extra space. However, nurses are concerned that if children move around without order, there will be problems with medical care and treatment.</p>"),
     ("Design Insights",
      quote("“Let's make the hallway a place for the children to play safely”")
      + "<h3>Nudge Design</h3><p>Nudge is a concept in behavioral science, political theory, and economics that proposes positive reinforcement and indirect suggestions to influence the behavior and decision-making of groups or individuals.</p>"
      + dimg_m("nud_di_1", "f4a835_6678c6a4c23543189a950b5aa29f8a53~mv2.jpg", "Nudge design in Amsterdam")
      + cap("Nudge design in Amsterdam: red lines suggest that visitors use the stairs rather than the lifts.")),
     ("Prototype & Testing",
      "<h3>Prototype 1: Making a Maze Prototype with Footprints</h3>"
      "<p>We used a maze, symbols, and footprints to encourage children to walk and stretch their legs.</p>"
      + dimg_m("nud_pt_1", "f4a835_bde2e20fcfd74040ba4b48d6e5711e3e~mv2.png", "Maze prototype")
      + "<h3>Prototype Testing at Kyeongdong Elementary School</h3>"
      "<p>We introduced the prototype to the children, who walked on it by following the lines, symbols, and footprints. After the test, we received feedback from the children. They wanted more complex missions and opportunities to play with friends.</p>"
      + dimg_m("nud_pt_2", "f4a835_36f7667148ac48c0b6e7c0c47eba6276~mv2.png", "Children walking on the prototype")
      + cap("Children walking on the prototype")
      + dimg_m("nud_pt_3", "f4a835_ef7ffcedd70e4a32976491bdc1e964f7~mv2.png", "Prototype 1 testing")
      + cap("Prototype 1 testing: children gave feedback about the prototype")
      + "<h3>Prototype 2</h3>"
      "<p>We added wallpapers to encourage various stretches. By adding a story to the wallpaper, children can also enjoy the story while they walk. The story is about a bird that gets sick and becomes healthy again with the help of its friends.</p>"
      + dimg_m("nud_pt_4", "f4a835_3476fbc9a8d44147bb19f2101f711c26~mv2.png", "Neck stretch wallpaper")
      + cap("Neck stretch: follow the birds trying to fly again! The child can naturally stretch their neck while following the birds in sequence.")
      + split(dimg_s("nud_pt_6", "f4a835_430c42386be14dbab4cb213bc914118a~mv2.png", "Different types of steps"),
              "<p><b>Different types of steps:</b> Children can follow the movements of animals and try different types of steps.</p>")
      + dimg_m("nud_pt_5", "f4a835_727a2a96f39e499fa9af98207b2a79e1~mv2.png", "Prototype 2 usability test")
      + "<h3>Prototype 2 Testing: Usability Test</h3>"
      "<p>We tested the prototype with Hyeon-Min (11 years old), and she enjoyed following the footprints. We asked her to carry a suitcase because we wanted to mimic the walking experience with an IV pole. She was able to walk the whole trail without difficulty. When she had a chance to modify the game, she participated actively and suggested different, interesting footsteps.</p>"),
     ("Outcome & Effects",
      "<p><b>Hospitalized children:</b> The aesthetically pleasing and playful wall prints can reduce negative images of hospitals. Through physical activity, children can improve their mental health and recover faster.</p>"
      "<p><b>Parents:</b> They are relieved because the prints act as a guideline. The child can safely play with the design. It may reduce the risk of secondary infections and accidents.</p>"
      "<p><b>Hospital:</b> The children walk the corridor in an orderly fashion, so there is no disruption to hospital work.</p>"
      + '<img class="reveal" src="assets/nud_hero.png" alt="Final nudge design" loading="lazy">')],
    awards="2017 KSDS Poster Honor Awards · 2017 Samsung Tomorrow Solution Finalist",
    hero=hero_img("nud_hero", "f4a835_f2d0d2cd57bc464ca212f9d517af2278~mv2.png", "Nudge design"))

MLH_HOW_TO_PLAY = """<p class="mlh-flow-intro">The hospitalized child plays with the participation and help of family members. Each person has a distinct role: the child becomes the immune-cell hero, the caregiver in the hospital serves as the DNA mentor, and family members outside the hospital support the quest as other cells such as neurons.</p>
<div class="mlh-play-diagram" aria-label="How the child and family members interact during the game">
  <div class="mlh-lifelines" aria-hidden="true"><span></span><span></span><span></span><span></span></div>
  <div class="mlh-flow-actors">
    <article class="mlh-actor"><img src="assets/optimized/mlh_hp_3.webp" alt="Child player" loading="lazy"><h3>Child in the hospital</h3><p>Immune-cell hero</p></article>
    <article class="mlh-actor"><img src="assets/optimized/mlh_hp_4.webp" alt="Caregiver staying with the child" loading="lazy"><h3>Caregiver in the hospital</h3><p>DNA mentor</p></article>
    <article class="mlh-actor"><img src="assets/optimized/mlh_hp_9.webp" alt="Caregiver outside the hospital" loading="lazy"><h3>Caregiver outside the hospital</h3><p>Quest supporter</p></article>
    <article class="mlh-actor"><img src="assets/optimized/mlh_hp_12.webp" alt="Sibling outside the hospital" loading="lazy"><h3>Sibling outside the hospital</h3><p>Neuron helper</p></article>
  </div>
  <div class="mlh-flow-timeline">
    <div class="mlh-stage"><article class="mlh-flow-step mlh-col-child"><span class="mlh-step-number">01</span><img src="assets/optimized/mlh_hp_5.webp" alt="Hero character customization screen" loading="lazy"><h3>Start the game</h3><p>The child defines a hero character and begins exploring the body.</p></article></div>
    <div class="mlh-stage"><article class="mlh-flow-step mlh-col-child"><span class="mlh-step-number">02</span><img src="assets/optimized/mlh_hp_6.webp" alt="The hero encounters a germ" loading="lazy"><h3>Meet the germ</h3><p>The hero encounters a germ and needs support from the family to fight it.</p></article></div>
    <div class="mlh-stage mlh-stage-message"><div class="mlh-message mlh-span-2 is-reverse"><span>DNA mentor → hero: advice and a quest</span></div></div>
    <div class="mlh-stage"><article class="mlh-flow-step mlh-col-child"><span class="mlh-step-number">03</span><img src="assets/optimized/mlh_hp_7.webp" alt="The DNA mentor explains how to defeat the germ" loading="lazy"><h3>Get help from the mentor</h3><p>The caregiver in the hospital explains how to defeat the germ and identifies the ingredients the hero needs.</p></article></div>
    <div class="mlh-stage mlh-stage-message"><div class="mlh-message mlh-span-3 is-forward"><span>Hero → outside caregiver: send a song quest</span></div></div>
    <div class="mlh-stage mlh-stage-message"><div class="mlh-message mlh-span-4 is-forward"><span>Hero → sibling: ask for help collecting honey</span></div></div>
    <div class="mlh-stage mlh-stage-parallel">
      <article class="mlh-flow-step"><span class="mlh-step-number">04A</span><img src="assets/optimized/mlh_hp_10.webp" alt="Song recording quest" loading="lazy"><h3>Sing a song to your father</h3><p>The caregiver receives the quest, hears the child's voice, and turns the recording into a bonding moment.</p></article>
      <article class="mlh-flow-step"><span class="mlh-step-number">04B</span><img src="assets/optimized/mlh_hp_13.webp" alt="Honey collection mini-game" loading="lazy"><h3>Collect honey</h3><p>The sibling plays a mini-game to collect honey for the child in the hospital.</p></article>
    </div>
    <div class="mlh-stage"><article class="mlh-flow-step mlh-col-outside"><span class="mlh-step-number">05</span><img src="assets/optimized/mlh_hp_11.webp" alt="Mini-game maze screen" loading="lazy"><h3>Unlock the mini-game</h3><p>When the caregiver receives the recording, the child's next mini-game becomes available.</p></article></div>
    <div class="mlh-stage mlh-stage-message"><div class="mlh-message mlh-span-3 is-reverse"><span>Outside caregiver → hero: recording received</span></div></div>
    <div class="mlh-stage mlh-stage-message"><div class="mlh-message mlh-span-4 is-reverse"><span>Sibling → hero: honey collected</span></div></div>
    <div class="mlh-stage mlh-stage-message"><div class="mlh-message mlh-span-2 is-reverse"><span>Caregiver in the hospital → hero: quest approved</span></div></div>
    <div class="mlh-stage"><article class="mlh-flow-step mlh-col-child"><span class="mlh-step-number">06</span><img src="assets/optimized/mlh_hp_8.webp" alt="Completed quest confirmation screen" loading="lazy"><h3>Finish the task</h3><p>With every ingredient collected and the quest approved, the hero defeats the germ and moves to the next level.</p></article></div>
    <div class="mlh-stage"><p class="mlh-flow-note">The game turns care into a shared family activity: the child leads the story, family members contribute short tasks, and every response helps the hero progress.</p></div>
  </div>
</div>"""

detail("mylittlehero.html", "My Little Hero", "UX Projects",
    [("Keywords", "Long-Term Hospitalized Children, Gamification, UX research, Storytelling, Family Engagement"),
     ("Members", "Personal Project"),
     ("My contribution", "UX research, UI design, Illustration"),
     ("Year", "2017")],
    "<p>‘My Little Hero’ is a digital game designed to facilitate communication between children who are hospitalized long term and their family members. It encourages all family members to play with the child and help them make progress in the game. The game's story was designed to help children and their family members understand the interactions between diseases and the immune system.</p>",
    [("What inspired this project",
      "<p>I heard a story from my friend about how long-term hospitalization caused her to become disconnected from her family when she was a child. She said long-term hospitalization makes a child lose touch with people outside the hospital. It makes it difficult for the child to share common interests with other family members. I decided to design an app that can connect families with children who are hospitalized long term.</p>"),
     ("App Summary",
      "<p><b>Reality:</b> If a child is hospitalized for a long time, communication among family members becomes limited and distant.</p>"
      "<p><b>Problem:</b> When a child is hospitalized for a long time, the family is divided into two groups. One group stays in the hospital to take care of the child, while the other group continues its normal life. The difference between the two groups grows as the hospital stay becomes longer. This results in separation between them. In many cases, this is traumatic for the child. The trauma can remain even after the child is discharged from the hospital.</p>"
      "<p><b>Solution:</b> I wanted to encourage communication among family members and create shared topics that can facilitate conversations. In the game, the child becomes an immune cell character and explores the body. Other family members also become immune cells or DNA and help the child's character overcome the disease in the game. This allows the child and family members to understand the immune system and build healthy habits.</p>"
      "<p><b>Importance:</b> Communication among family members can prevent trauma caused by disconnection. The child can also build healthy habits through the game.</p>"),
     ("Problems",
      "<h3>Problems caused by a child's long-term hospitalization</h3>"
      "<p><b>Separation of family:</b> The family is divided into a group that provides care and a group that continues its normal life, resulting in separation between the two.</p>"
      "<p><b>Lack of stimulation through play:</b> Although children need a variety of stimuli, it is difficult for them to play in hospitals.</p>"
      "<p><b>A lack of understanding of disease:</b> The child does not understand why their body is sick or how their organs work. As a result, the treatment process becomes more difficult and painful. Young siblings may also feel jealous of or harass their sick sibling because they do not understand why the sibling is hospitalized.</p>"
      + dimg_m("mlh_pr_1", "f4a835_dfb7c187f9e54d42829e2eac3a51c60f~mv2.png", "Problems")
      + row("c3",
            dimg_s("mlh_pr_2", "f4a835_2320f3c512bd4870a7312b2bbee48b6a~mv2.png", "Separation of family"),
            dimg_s("mlh_pr_3", "f4a835_92bec3806eb24a7890032462bc6de56e~mv2.png", "Lack of stimulation"),
            dimg_s("mlh_pr_4", "f4a835_8d015a35285e4b9e81ef03cb1b821f80~mv2.png", "Lack of understanding"))),
     ("Design Insights",
      "<h3>Digital Solution to Connect Family</h3>"
      "<p>A family is divided into two groups: one that belongs to the hospital and another that belongs to everyday life. As the hospitalization becomes longer, they have less common ground to share.</p>"
      + quote("“Let's make a family game that all family members can enjoy and use to share common subjects.”")
      + "<h3>1. Increase Self-Confidence by Using the ‘Hero's Journey’ Structure</h3>"
      "<p>The process of a child fighting germs and becoming healthy seemed similar to that of an ordinary character becoming a hero in a heroic myth. Therefore, I decided to use the structure of the ‘Hero's Journey’.</p>"
      "<p><b>Effects, Fun:</b> The heroic myth has long provided an interesting structure for readers. The structure helps keep readers interested in the story. <b>Recovering self-esteem:</b> Through the process of becoming a hero, the child overcomes feelings of helplessness and restores confidence.</p>"
      + dimg_m("mlh_di_1", "f4a835_d706aee092ca4c618d402ec0c303f6b2~mv2.png", "Hero's journey structure")
      + dimg_m("mlh_di_2", "f4a835_03d84ef49183450898f1f2e51e4cb5ef~mv2.png", "Structure of the hero myth")
      + "<h3>2. Understanding How the Body Works</h3>"
      "<p><b>Become an immune cell in the game:</b> The child explores the whole body by becoming an immune cell in the game. The character fights germs and meets other helpful immune cells.</p>"
      "<p><b>Effects, Understanding the body:</b> Children and their families can naturally learn about the body's immune system and organs. This helps children understand the treatment they receive at the hospital.</p>"
      + dimg_m("mlh_di_3", "f4a835_c811f4eb0686424e8211f15a1805c385~mv2.jpg", "Immune cell")
      + dimg_m("mlh_di_4", "f4a835_5a490410bd504422b6e3212c09968665~mv2.png", "Exploring the body")
      + "<h3>3. Family Sends Quests to Each Other to Entertain and Acquire Healthy Habits</h3>"
      "<p><b>Quest:</b> “Sing a song to your father! He will confirm that you finished the quest!” By singing a song to the father, the child can strengthen the family bond, and the father helps with the child's gameplay by approving the quest. The child can feel supported by the family.</p>"
      "<p><b>Quest:</b> “To win the fight against the cold germ, you have to get ginger tea! Ask your sister for help.” By receiving a quest related to a healthy lifestyle, a child can learn about healthy habits while playing the game.</p>"
      + dimg_m("mlh_di_5", "f4a835_212e53b3c0c04d25a61f7a032757f8b2~mv2.png", "Quests between family")
      + dimg_m("mlh_di_6", "f4a835_c290984ad4104bb5a2033d4b0bdda1ec~mv2.png", "Quest examples")
      + "<h3>4. Receiving Support</h3>"
      "<p>A family member plays the role of a supporter in the game. They collaborate whenever they encounter germs in the game to solve problems. Through this collaboration, they can finish the game and win the fight.</p>"
      + dimg_s("mlh_di_7", "f4a835_a059dc75adab46c39bfe489c48181c26~mv2.png", "Receiving support")
      + "<h3>Solution</h3>"
      "<p>A digital game that the whole family can play together to understand the child's diseases and circumstances. Parents can participate in their daily lives because their roles are those of helpers and supporters. Their part consists of easy tasks, such as approving a child's requests or playing a mini-game.</p>"),
     ("Design",
      "<h3>Concept Sketch</h3>"
      "<p>Sketch of one of the minigames, early character designs for immune cells, and a sketch of the game's background map. Based on scientific facts, I designed immune cells according to their functions in the body. For example, macrophages that eat germs are drawn as chubby characters that like to eat (top left).</p>"
      + dimg_m("mlh_de_1", "f4a835_70a132779a034caf82a1934b91a30078~mv2.png", "Concept sketch")
      + row("", dimg_s("mlh_de_2", "f4a835_f24f3a3e7cce4fe0bc5417cc06c40eab~mv2.png", "Character sketches"),
               dimg_s("mlh_de_3", "f4a835_f24f253ba29e41b483ffdbaea47ec654~mv2.png", "Background map sketch"))
      + "<h3>Character Design</h3>"
      "<p>Main character, immune cells, DNA, and neuron characters. The hospitalized child becomes the main character (top left) and the game's primary immune cell (bottom left). Parents become DNA, and siblings can choose the immune cells they want to be, except for the main immune cell.</p>"
      + dimg_m("mlh_de_4", "f4a835_dc178de3f55845ddba6537064c928200~mv2.png", "Character design")
      + "<h3>Mood Board</h3>"
      "<p>To convey the feeling of being inside the body, I set red as the main color. The characters are designed in a simple style to appeal to children.</p>"
      + dimg_m("mlh_de_5", "f4a835_e250330849844bba87e630ba585a3262~mv2.png", "Mood board")
      + "<h3>Final Design</h3>"
      + dimg_m("mlh_de_7", "f4a835_e1e40395fa05489797bd82ced5167ad3~mv2.png", "Final design screens")
      + dimg_s("mlh_de_6", "f4a835_ec514a08c86d4a669fe3ae0c934aeff3~mv2.png", "Final design")),
     ("How to play", MLH_HOW_TO_PLAY)],
    hero=hero_img("mlh_hero", "f4a835_235d6c02d9f14eddafb5032202f6c247~mv2.png", "My Little Hero"))

detail("sunshine.html", "Sunshine", "UX Projects",
    [("Keywords", "Digital Window, Sunlight, Multisense"),
     ("Members", "Personal Project"),
     ("My contribution", "UX / Product design"),
     ("Year", "4.2017 – 6.2017")],
    "<p>‘Sunshine’ is an IoT device. Digital lighting can change the view, and users can experience corresponding scents, sounds, and breezes. A user can choose a place on their smart device, and the digital window displays the view selected in the app. The user can also adjust the levels of light, breeze, scent, and sound. The fan is located inside the frame, so it can purify the indoor air and send it out like a breeze from the window.</p>",
    [], hero=hero_img("sun_hero", "f4a835_b5f05335dd2e4f04a25119a39e2fc238~mv2.png", "Sunshine"))

TOMORROW_DESIGN = (
    "<p class=\"tmr-design-intro\">The service has two connected versions: one for French citizens who donate unused devices or record stories, and one for refugee children who learn French and coding through those stories.</p>"
    "<div class=\"tmr-role-flow\">"
    "<article class=\"tmr-role-row reveal\">"
    "<figure class=\"tmr-role-figure\">"
    + dimg_m("tmr_d_1", "f4a835_d8f11d16649442058c5a3113a3f37ff7~mv2.png", "Donor app screens")
    + "</figure>"
    "<div class=\"tmr-role-copy\"><span class=\"tmr-role-kicker\">French citizen</span><h3>Donor</h3>"
    "<ol class=\"tmr-step-list\"><li>Donate unused smart devices to refugee children.</li><li>Record a French audiobook for a child to listen to.</li></ol>"
    "</div></article>"
    "<article class=\"tmr-role-row reveal\">"
    "<figure class=\"tmr-role-figure\">"
    + dimg_m("tmr_d_2", "f4a835_a790961de54f4bbfb73bd6b53259a886~mv2.png", "Refugee child app screens")
    + "</figure>"
    "<div class=\"tmr-role-copy\"><span class=\"tmr-role-kicker\">Learner</span><h3>Refugee child</h3>"
    "<ol class=\"tmr-step-list\"><li>Read a children's book while learning French and coding.</li><li>Unlock and read more interactive books.</li><li>Join learning events created for children.</li></ol>"
    "</div></article></div>"
    "<article class=\"tmr-reading-flow reveal\">"
    "<div class=\"tmr-reading-head\"><span class=\"tmr-role-kicker\">Learning interface</span><h3>Reading Page</h3></div>"
    + dimg("tmr_d_3", "f4a835_21bcd67af3e5478f81f8e80632e63986~mv2.png", "Interactive reading page")
    + "<ol class=\"tmr-reading-steps\"><li>Study French through dialogue in the book.</li><li>Learn coding with simple block-based coding methods.</li><li>Fill in the blank with the correct French word.</li><li>See the Little Prince react, then continue the story.</li></ol>"
    "</article>"
)

detail("tomorrow.html", "Tomorrow", "UX Projects",
    [("Keywords", "Refugee Children, Coding Education, French Education, Interaction"),
     ("Members", "Personal Project"),
     ("My contribution", "UX research, UI design"),
     ("Year", "6.2017")],
    "<p>‘Tomorrow’ is a service designed to teach coding and French to refugee children in France through French children's books. After receiving a smart device from a donor, children learn French and coding simultaneously through French children's books. Using block-based coding methods, children can easily make interactive storybooks.</p>",
    [("What inspired this project",
      "<p>While I was traveling in Paris, I witnessed conflicts between locals and refugees. There were police officers at the museums and the Eiffel Tower. I wondered whether technology could help ease these conflicts. After some research, I found that many refugees had difficulty adjusting to French society because of the language. Many of them also did not have a chance to attend school. Meanwhile, Europe needed more IT experts. I wanted to help refugee children through an app that they could use to learn French and coding together.</p>"),
     ("Service Summary",
      "<p><b>Reality:</b> In France, many refugees cannot adjust to society, so social conflicts are widespread. This creates tension in society.</p>"
      "<p><b>Problem:</b> Refugee children in France do not have enough educational opportunities, and because they cannot speak French, they cannot socialize with their peers and may feel alienated. In addition, they may have trauma from the war.</p>"
      "<p><b>Solution:</b> Refugee children can use French children's books to learn French, which can help them adjust to society. Because classic children's books are no longer under copyright, children can use them for free. With help and donations from French citizens, children can receive French audiobooks recorded by citizens and donated cellphones for studying. They can enjoy the learning process while making the books interactive.</p>"
      "<p><b>Importance:</b> The service can contribute to a more harmonious society and support the education of refugee children. IT education can also help address Europe's workforce shortage.</p>"),
     ("Design", TOMORROW_DESIGN)],
    hero=hero_img("tmr_hero", "f4a835_ff310f1c911b4a118aa6d9619bfe9afa~mv2.png", "Tomorrow"))

# Public filename contract: do not rename pmos-comics.html.
detail("pmos-comics.html", "PMOS.Comics", "UX Projects · Series",
    [("Project type", "Interactive comics series"),
     ("Status", "In development"),
     ("Year", "2026 – Present")],
    "<p>Project description will be added here.</p>",
    [("Overview",
      '<div class="project-content-placeholder"><p>Project overview will be added here.</p></div>'),
     ("Design Process",
      '<div class="project-content-placeholder"><p>Design process and project materials will be added here.</p></div>'),
     ("Outcomes",
      '<div class="project-content-placeholder"><p>Project outcomes will be added here.</p></div>')],
    hero='<div class="bleed detail-placeholder-hero" role="img" aria-label="PMOS.Comics hero image to be added"></div>')

# Permanent public filename contracts: these pages are linked from the CV.
PROJECT_PLACEHOLDER_SECTIONS = [
    ("Overview", '<div class="project-content-placeholder"><p>Project overview will be added here.</p></div>'),
    ("Design Process", '<div class="project-content-placeholder"><p>Design process and project materials will be added here.</p></div>'),
    ("Outcomes", '<div class="project-content-placeholder"><p>Project outcomes will be added here.</p></div>'),
]

THEMEVIZ_SECTIONS = [
    ("Background", """
        <p>Thematic analysis is a research method used to identify patterns or themes within qualitative data. It is widely used in scientific research, user research, and product development, but it is also notoriously time-consuming and laborious.</p>
        <div class="themeviz-phases" aria-label="Six phases of thematic analysis">
          <article><img src="assets/originals/themeviz/six-phases/phase-1.png?v=20260824" alt="Illustration of a researcher reading transcripts"><div class="themeviz-phase-label"><span class="themeviz-phase-number">01</span><strong>Reading transcripts</strong></div></article>
          <article><img src="assets/originals/themeviz/six-phases/phase-2.png?v=20260824" alt="Illustration of excerpts being assigned qualitative codes"><div class="themeviz-phase-label"><span class="themeviz-phase-number">02</span><strong>Coding</strong></div></article>
          <div class="themeviz-phase-group"><span>Theme development steps</span></div>
          <article class="is-theme-development"><img src="assets/originals/themeviz/six-phases/phase-3.png?v=20260824" alt="Illustration of codes being grouped while searching for themes"><div class="themeviz-phase-label"><span class="themeviz-phase-number">03</span><strong>Searching for themes</strong><span class="themeviz-phase-category">Theme development step</span></div></article>
          <article class="is-theme-development"><img src="assets/originals/themeviz/six-phases/phase-4.png?v=20260824" alt="Illustration of code groups being reviewed and reorganized"><div class="themeviz-phase-label"><span class="themeviz-phase-number">04</span><strong>Reviewing themes</strong><span class="themeviz-phase-category">Theme development step</span></div></article>
          <article class="is-theme-development"><img src="assets/originals/themeviz/six-phases/phase-5.png?v=20260824" alt="Illustration of themes and sub-themes being defined"><div class="themeviz-phase-label"><span class="themeviz-phase-number">05</span><strong>Defining themes</strong><span class="themeviz-phase-category">Theme development step</span></div></article>
          <article><img src="assets/originals/themeviz/six-phases/phase-6.png?v=20260824" alt="Illustration of a researcher reporting thematic analysis findings"><div class="themeviz-phase-label"><span class="themeviz-phase-number">06</span><strong>Reporting</strong></div></article>
        </div>
        <p class="themeviz-reference">Figure. Six-phase framework (Braun and Clarke, 2012).</p>
        <p>Previous computational research has largely focused on coding because it involves relatively clear tasks, such as labeling data with a predefined codebook. Theme development is harder to support. Searching for, reviewing, and defining themes require researchers to abstract, synthesize, and interpret meaning across a dataset.</p>
        <p>This work becomes more challenging because researchers often create and compare multiple versions of themes before identifying the interpretation that best represents their data. LLMs can support this conceptual work by understanding text and developing candidate themes. More importantly, they may act as research collaborators by offering alternative interpretations of the data that researchers may not have initially considered.</p>
        <p>ThemeViz investigates whether a purpose-built interface can turn these capabilities into meaningful human-AI collaboration during theme development.</p>"""),
    ("Research Questions", """
        <div class="themeviz-rq-list">
          <article><div class="themeviz-rq-label">RQ1</div><p>How useful is ThemeViz for theme development compared with a conventional prompting interface such as ChatGPT?</p></article>
          <article><div class="themeviz-rq-label">RQ2</div><p>To what extent does ThemeViz&rsquo;s design encourage users to view its AI assistant as a collaborative partner in theme development compared with a traditional interface such as ChatGPT?</p></article>
        </div>"""),
    ("Design Goals", """
        <p>The following three design goals guided the system&rsquo;s design.</p>
        <div class="themeviz-goals">
          <article><div class="themeviz-goal-number">01</div><h3>Support user autonomy</h3><p>Qualitative researchers often resist fully automated analysis and want to remain responsible for interpretation. ThemeViz therefore preserves manual coding and manual theme development so researchers maintain control of the analysis.</p></article>
          <article><div class="themeviz-goal-number">02</div><h3>Promote sensemaking</h3><p>Researchers often use visual media such as theme maps to understand relationships within data. Instead of returning long blocks of model-generated text, ThemeViz uses interactive bubble charts to make themes easier to inspect and compare.</p></article>
          <article><div class="themeviz-goal-number">03</div><h3>Reduce prompting overhead</h3><p>Passing long text, metadata, and prior analysis back and forth through a chat interface is burdensome. ThemeViz centrally manages transcripts, user-generated codes, metadata, and prompts so researchers can focus on developing themes.</p></article>
        </div>"""),
    ("System Design", """
        <p>ThemeViz supports the full analysis workflow while focusing AI assistance on searching for, reviewing, and defining themes. Researchers retain the ability to code and develop themes manually, then work with GPT-4 to generate and refine alternative theme structures.</p>
        <div class="themeviz-system-flow" aria-label="ThemeViz analysis workflow">
          <article class="themeviz-system-step">
            <div class="themeviz-browser-frame"><div class="themeviz-browser-toolbar" aria-hidden="true"><span></span></div><div class="themeviz-system-video-crop"><video autoplay muted loop playsinline preload="metadata" poster="assets/originals/themeviz/system-design/manual-coding.png"><source src="assets/originals/themeviz/system-design/manual-coding.mp4" type="video/mp4">Your browser does not support this video.</video></div></div>
            <div class="themeviz-system-step-copy"><div class="themeviz-system-step-number">1</div><h3>Manual coding</h3><p>On the coding page, users highlight text segments that capture key ideas. They can assign new codes or select existing codes from a dropdown menu. Codes are assigned to individual rows.</p></div>
          </article>
          <article class="themeviz-system-step">
            <div class="themeviz-browser-frame"><div class="themeviz-browser-toolbar" aria-hidden="true"><span></span></div><div class="themeviz-system-video-crop"><video autoplay muted loop playsinline preload="metadata" poster="assets/originals/themeviz/system-design/manual-theme-development.png"><source src="assets/originals/themeviz/system-design/manual-theme-development.mp4" type="video/mp4">Your browser does not support this video.</video></div></div>
            <div class="themeviz-system-step-copy"><div class="themeviz-system-step-number">2</div><h3>Manual theme development</h3><p>On the left side of the page, ungrouped code&ndash;text pairs include both coded and uncoded data, with codes highlighted in yellow. Users create themes by selecting &ldquo;Add Theme,&rdquo; then drag and drop code&ndash;text pairs from the left panel into a theme box.</p></div>
          </article>
          <article class="themeviz-system-step is-ai-step">
            <div class="themeviz-browser-frame"><div class="themeviz-browser-toolbar" aria-hidden="true"><span></span></div><div class="themeviz-system-video-crop"><video autoplay muted loop playsinline preload="metadata" poster="assets/originals/themeviz/system-design/iterative-theme-development-ai.png"><source src="assets/originals/themeviz/system-design/iterative-theme-development-ai.mp4" type="video/mp4">Your browser does not support this video.</video></div></div>
            <div class="themeviz-system-step-copy"><div class="themeviz-system-step-number">3</div><h3>Iterative theme development with&nbsp;AI</h3><p>The left side of the page presents theme titles, theme explanations, and the code&ndash;text pairs assigned to each theme. On the right, an interactive bubble chart visualizes themes and their code&ndash;text pairs.</p></div>
          </article>
        </div>"""),
    ("Iterative Theme Development with&nbsp;AI", """
        <div class="themeviz-ai-page-detail" aria-labelledby="themeviz-ai-detail-title">
          <h3 id="themeviz-ai-detail-title">Interface details</h3>
          <div class="themeviz-annotated-interface">
            <div class="themeviz-interface-top-callouts">
              <article class="themeviz-interface-callout"><div class="themeviz-interface-callout-heading"><span class="themeviz-interface-marker">3</span><h4>Prompt the AI</h4></div><p>Users can describe how they want the AI to generate themes in the text input box.</p></article>
              <article class="themeviz-interface-callout"><div class="themeviz-interface-callout-heading"><span class="themeviz-interface-marker">4</span><h4>Generate themes</h4></div><p>Selecting &ldquo;AI assistance&rdquo; generates a new set of themes.</p></article>
              <article class="themeviz-interface-callout"><div class="themeviz-interface-callout-heading"><span class="themeviz-interface-marker">5</span><h4>Set theme count</h4></div><p>The slider adjusts the desired number of themes.</p></article>
            </div>
            <article class="themeviz-interface-callout themeviz-interface-callout-left"><div class="themeviz-interface-callout-heading"><span class="themeviz-interface-marker">1</span><h4>Theme details</h4></div><p>The left side presents theme titles, explanations, and the code&ndash;text pairs assigned to each theme.</p></article>
            <figure><img src="assets/originals/themeviz/system-design/phase3_version2.png?v=20260825" alt="Annotated ThemeViz interface showing theme details, linked selections, an interactive bubble chart, an AI prompt, an AI assistance button, and a theme-count slider"></figure>
            <article class="themeviz-interface-callout themeviz-interface-callout-right"><div class="themeviz-interface-callout-heading"><span class="themeviz-interface-marker">2 / 2a</span><h4>Interactive themes and codes</h4></div><p>On the right, outer circles represent themes and color-coded bubbles represent code&ndash;text pairs. Linked interactions highlight connections between the two panels.</p></article>
          </div>
        </div>
        <article class="themeviz-demo">
          <div class="themeviz-demo-copy"><div class="themeviz-demo-number">01</div><h3>Adjust theme granularity</h3><p>A slider changes the requested number of themes. A smaller number produces broader, higher-level themes; a larger number produces more specific and granular themes.</p></div>
          <video controls muted playsinline preload="metadata" poster="assets/originals/themeviz/theme-granularity-poster.png"><source src="assets/originals/themeviz/theme-granularity.mp4" type="video/mp4">Your browser does not support this video.</video>
        </article>
        <article class="themeviz-demo">
          <div class="themeviz-demo-copy"><div class="themeviz-demo-number">02</div><h3>Guide the AI with custom prompts</h3><p>Researchers can direct the model toward a particular analytical lens. For example, they can ask it to focus on an interviewee&rsquo;s relationship with her parents and her personality, then inspect the newly generated themes.</p></div>
          <video controls muted playsinline preload="metadata" poster="assets/originals/themeviz/custom-prompts-poster.png"><source src="assets/originals/themeviz/custom-prompts.mp4" type="video/mp4">Your browser does not support this video.</video>
        </article>
        <article class="themeviz-demo">
          <div class="themeviz-demo-copy"><div class="themeviz-demo-number">03</div><h3>Examine theme quality</h3><p>Researchers can interact with the bubble chart at any time to inspect which codes belong to each AI-generated theme and judge whether the proposed structure is coherent.</p></div>
          <video controls muted playsinline preload="metadata" poster="assets/originals/themeviz/theme-quality-third-poster.png?v=20260824-third"><source src="assets/originals/themeviz/theme-quality-third.mp4?v=20260824-third" type="video/mp4">Your browser does not support this video.</video>
        </article>"""),
    ("Study", """
        <p>We conducted a between-subjects study with 28 participants, randomly assigning 14 participants to each condition. Both conditions used the same GPT-4 model so that the comparison focused on interaction design rather than model capability.</p>
        <div class="themeviz-condition-grid">
          <article><h3>ChatGPT condition</h3><p>Participants used Atlas.ti for coding and initial theme development, then used ChatGPT for AI-assisted theme development.</p></article>
          <article><h3>ThemeViz condition</h3><p>Participants used ThemeViz for coding, initial theme development, and AI-assisted theme development within one integrated workflow.</p></article>
        </div>
        <p>Each session included 10 minutes of coding, 5 minutes of initial theme development, 20 minutes of AI-assisted theme development, 5 minutes to finalize themes and complete a survey, and a 10-minute interview.</p>
        <figure class="themeviz-figure"><img src="assets/originals/themeviz/study-design.png" alt="Between-subjects study design comparing ChatGPT and ThemeViz conditions with 28 participants"></figure>"""),
    ("Findings", """
        <h3>RQ1: ThemeViz was more useful than a traditional ChatGPT interface</h3>
        <p>ThemeViz users created more theme iterations and developed more diverse perspectives from the dataset. They also found that its interactive visualization helped them comprehend the data and rated the visual output as more useful than ChatGPT&rsquo;s text-based responses.</p>
        <figure class="themeviz-figure themeviz-result-figure"><img src="assets/originals/themeviz/results-rq1-selected.png?v=20260824-rq-crops" alt="RQ1 bar charts showing more theme iterations and perspectives and higher ratings for data comprehension and visual output usefulness with ThemeViz than with ChatGPT"></figure>
        <p class="themeviz-result-interpretation">Together, these differences suggest that ThemeViz supported both exploration and sensemaking: participants considered more possible theme structures while using the visualization to understand and compare the underlying data.</p>
        <h3>RQ2: Interaction design shaped perceptions of collaboration</h3>
        <p>Participants rated ThemeViz&rsquo;s assistant significantly higher as a collaborator and in its ability to collaborate than the same AI model presented through ChatGPT.</p>
        <figure class="themeviz-figure themeviz-result-figure themeviz-result-figure--rq2"><img src="assets/originals/themeviz/results-rq2-collaboration.png?v=20260824-rq-crops" alt="RQ2 bar charts showing higher collaborator and collaborative ability ratings for ThemeViz than for ChatGPT"></figure>
        <p class="themeviz-result-interpretation">Because both conditions used GPT-4, these results suggest that interaction design—not model capability alone—shaped how collaborative the AI felt. Even with these higher ratings, participants did not fully consider the AI a true collaborator. Our interviews revealed concerns about the AI&rsquo;s lack of agency and responsibility. Participants also pointed to limitations in the AI&rsquo;s passive communication style. They felt that simply seeing potential themes was not enough to support deeper thinking.</p>
        <div class="themeviz-quote-grid">
          <blockquote><p>&ldquo;AI assistant does not have its own &lsquo;mindset&rsquo; while human collaborators have their own.&rdquo;</p><cite>P10</cite></blockquote>
          <blockquote><p>&ldquo;Being a collaborator implies that it has agency and can share responsibility for those mistakes or incorrect information. However, I don&rsquo;t think it has that responsibility.&rdquo;</p><cite>P23</cite></blockquote>
          <blockquote><p>&ldquo;Good collaboration is like two people who either argue with each other or challenge each other to think, to create something new.&rdquo;</p><cite>P24</cite></blockquote>
        </div>"""),
    ("Design Implications", """
        <div class="themeviz-implications">
          <article><div class="themeviz-goal-number">01</div><h3>Support researcher autonomy</h3><p>AI lacks agency and responsibility. When AI can produce negative or misleading outcomes, researchers need clear control over their analytical process and final interpretations.</p></article>
          <article><div class="themeviz-goal-number">02</div><h3>Design for proactive communication</h3><p>Questions and constructive challenges can deepen reflection. Future systems should explore questioning AI agents that prompt researchers to examine assumptions and think critically during theme development.</p></article>
        </div>
        <p class="themeviz-paper-cta"><a href="https://dl.acm.org/doi/10.1145/3757675" target="_blank" rel="noopener">Read the full ThemeViz paper →</a></p>"""),
]

# Mindful is a hand-authored long-form case study based on two research papers.
# Keep the generated site from replacing its portfolio narrative with a generic
# placeholder during routine rebuilds. The committed HTML remains the source for
# that page, just as the teaching portfolio is preserved above.
mindful_path = os.path.join(ROOT, "mindful-journaling.html")
if not os.path.exists(mindful_path):
    detail("mindful-journaling.html", "Mindful", "UX Projects",
        [("Keywords", "Human-AI interaction, Expressive writing, Reflection, Generative AI"),
         ("Members", "Daye Kang, Wenhan Dong, Swati Mishra"),
         ("My contribution", "<strong>Lead Researcher &amp; Designer</strong><br>Research framing, interaction and system design, responsible-AI workflow, study design, and qualitative analysis"),
         ("Year", "2025")],
        '<p class="mindful-deck">AI-Assisted Journaling for Reflection</p>',
        [("Project Story", "<p>This long-form portfolio story is maintained in mindful-journaling.html.</p>")],
        hero='<div class="bleed mindful-hero"><img src="assets/originals/mindful/mindful-workflow.png?v=20260824" alt="Four-step Mindful workflow from journal writing to AI-assisted reflection and mood review"></div>')

detail("themeviz.html", "ThemeViz", "UX Projects",
    [("Keywords", "Human-AI collaboration, Qualitative data analysis, Theme development, LLMs"),
     ("Members", "Daye Kang, Zhuolun Han, Jiahe Tian, Muhan Zhang, Jeff Rzeszotarski"),
     ("My contribution", "Lead Researcher<br>Research framing, study design, system design and development, data visualization, study execution, and data analysis"),
     ("Year", "2023")],
    "<p>LLM-Enhanced Visual System for Theme Development</p>",
    THEMEVIZ_SECTIONS,
    awards='Best Paper Honorable Mention Award, ACM CSCW 2025<br><a class="meta-paper-link" href="https://dl.acm.org/doi/10.1145/3757675" target="_blank" rel="noopener">See published paper →</a>',
    hero='<div class="bleed themeviz-hero"><img src="assets/banner10.png?v=20261013" alt="ThemeViz interface displayed on a laptop"></div>')

detail("toonnote.html", "ToonNote", "UX Projects",
    [("Keywords", "Interactive data comics, Computational notebooks, Data storytelling"),
     ("Members", "Daye Kang, Tony Ho, Nicolai Marquardt, Bilge Mutlu, Andrea Bianchi"),
     ("My contribution", "Research, system design and development, usability evaluation"),
     ("Year", "2020")],
    "<p>Interactive Data Comics for Computational Notebooks</p>",
    PROJECT_PLACEHOLDER_SECTIONS,
    hero='<div class="bleed detail-placeholder-hero" role="img" aria-label="ToonNote representative image to be added"></div>')

# ================= MANIFEST + DOWNLOAD SCRIPT =================
with open(os.path.join(ROOT, "assets_manifest.txt"), "w") as f:
    for local, url in sorted(MANIFEST.items()):
        f.write(f"{local}\t{url}\n")

W("download_assets.sh", """#!/bin/bash
# Downloads every image/PDF listed in assets_manifest.txt into assets/.
# Safe to re-run: already-downloaded files are skipped.
cd "$(dirname "$0")"
total=0; ok=0; fail=0
while IFS=$'\\t' read -r name url; do
  [ -z "$name" ] && continue
  total=$((total+1))
  dest="assets/$name"
  mkdir -p "$(dirname "$dest")"
  if [ -s "$dest" ]; then ok=$((ok+1)); continue; fi
  got=0
  if curl -fsSL --retry 2 -o "$dest" "$url"; then got=1; fi
  if [ "$got" = "0" ] && echo "$url" | grep -q "video.wixstatic.com"; then
    for q in 720p 360p 1080p; do
      alt="${url/480p/$q}"
      if curl -fsSL -o "$dest" "$alt"; then got=1; echo "     ($name: used $q)"; break; fi
    done
  fi
  if [ "$got" = "1" ]; then
    ok=$((ok+1)); echo "ok   $name"
  else
    rm -f "$dest"; fail=$((fail+1)); echo "FAIL $name  <-  $url"
  fi
done < assets_manifest.txt
echo "----------------------------------------"
echo "done: $ok/$total downloaded, $fail failed"
""")

print(f"built {len([f for f in os.listdir(ROOT) if f.endswith('.html')])} pages, {len(MANIFEST)} assets in manifest")
