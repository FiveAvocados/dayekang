(function () {
  const section = id => document.getElementById(id);
  const direct = (root, selector) => [...root.children].filter(el => el.matches(selector));
  const image = (root, name) => root.querySelector(`img[src*="/${name}."]`);
  const heading = (root, text) => direct(root, 'h3').find(el => el.textContent.trim().startsWith(text));

  function enhanceBackground() {
    const root = section('s2');
    if (!root || root.querySelector('.lexia-background-overview')) return;
    const [stats, hangeul] = direct(root, 'img');
    const [statsCopy, hangeulCopy] = direct(root, 'p');
    const overview = document.createElement('div');
    overview.className = 'lexia-background-overview';
    const copy = document.createElement('div');
    copy.className = 'lexia-stat-copy';
    copy.innerHTML = '<p>Around 5 to 10 percent of children worldwide have dyslexia.</p><p>Of the 50 million people in Korea, 5 million have dyslexia.</p><p>The Korean language has its own writing and pronunciation systems.</p>';
    overview.append(stats, copy);
    const figure = document.createElement('figure');
    figure.className = 'lexia-hangeul';
    const caption = document.createElement('figcaption');
    caption.textContent = 'Korean characters are called Hangeul, and their shapes are based on the shape of the mouth when making sounds.';
    figure.append(hangeul, caption);
    statsCopy.remove();
    hangeulCopy.remove();
    root.append(overview, figure);
  }

  function enhanceProblems() {
    const root = section('s3');
    if (!root || root.querySelector('.lexia-problem-grid')) return;
    const list = root.querySelector(':scope > ul');
    const summary = root.querySelector(':scope > p');
    const illustration = root.querySelector(':scope > img');
    illustration.classList.add('lexia-problem-illustration');
    const grid = document.createElement('div');
    grid.className = 'lexia-problem-grid';
    [...list.children].forEach(item => {
      const article = document.createElement('article');
      const title = document.createElement('h3');
      const body = document.createElement('p');
      title.textContent = item.querySelector('b').textContent;
      body.textContent = item.textContent.replace(title.textContent, '').replace(/^\s*[:—-]\s*/, '');
      article.append(title, body);
      grid.append(article);
    });
    summary.classList.add('lexia-problem-summary');
    list.replaceWith(illustration, grid);
    grid.after(summary);
  }

  function enhanceDyslexia() {
    const root = section('s4');
    if (!root || root.querySelector('.lexia-dyslexia-hero')) return;
    const titles = direct(root, 'h3');
    const paragraphs = direct(root, 'p');
    const [hero, brain, treatment] = direct(root, 'img');
    const list = root.querySelector(':scope > ul');
    hero.classList.add('lexia-dyslexia-hero');
    brain.classList.add('lexia-brain-chart');
    const copy = document.createElement('div');
    copy.className = 'lexia-dyslexia-copy';
    titles.slice(0, 3).forEach((title, index) => copy.append(title, paragraphs[index]));
    titles[3].classList.add('lexia-treatment-title');
    const treatmentGrid = document.createElement('div');
    treatmentGrid.className = 'lexia-treatment-grid';
    const treatmentCopy = document.createElement('div');
    const ordered = document.createElement('ol');
    [...list.children].forEach(item => ordered.append(item));
    treatmentCopy.append(paragraphs[3], ordered);
    treatmentGrid.append(treatment, treatmentCopy);
    list.remove();
    root.append(hero, copy, brain, titles[3], treatmentGrid);
  }

  function makePersona(root, title, split, label) {
    const card = document.createElement('section');
    card.className = 'lexia-persona';
    const name = title.textContent.replace(/^Persona \d+\s*:\s*/, '').trim();
    title.textContent = label;
    title.className = 'lexia-persona-kicker';
    split.className = 'lexia-persona-grid';
    const copy = split.children[1];
    const nameHeading = document.createElement('h4');
    nameHeading.textContent = name;
    copy.prepend(nameHeading);
    const first = copy.querySelector('p');
    const thinkingMarker = '<b>Thinking:</b>';
    if (first && first.innerHTML.includes(thinkingMarker)) {
      const [situation, thinking] = first.innerHTML.split(thinkingMarker);
      first.innerHTML = situation;
      const thinkingParagraph = document.createElement('p');
      thinkingParagraph.innerHTML = thinkingMarker + thinking;
      first.after(thinkingParagraph);
    }
    const needs = [...copy.querySelectorAll('p')].find(p => p.textContent.trim().startsWith('Needs:'));
    if (needs) {
      const needsHeading = document.createElement('h4');
      needsHeading.className = 'lexia-needs-heading';
      needsHeading.textContent = 'Needs';
      const list = document.createElement('ol');
      needs.textContent.replace(/^Needs:\s*/, '').split(/\s+(?=\d\)\s)/).forEach(item => {
        const li = document.createElement('li');
        li.textContent = item.replace(/^\d\)\s*/, '');
        list.append(li);
      });
      needs.replaceWith(needsHeading, list);
    }
    root.insertBefore(card, title);
    card.append(title, split);
    return card;
  }

  function enhanceResearch() {
    const root = section('s5');
    if (!root || root.querySelector('.lexia-persona')) return;
    const personaOneTitle = heading(root, 'Persona 1');
    const personaTwoTitle = heading(root, 'Persona 2');
    const experienceTitle = heading(root, 'Experience Mapping');
    if (!personaOneTitle || !personaTwoTitle || !experienceTitle) return;
    const personaHeading = document.createElement('h3');
    personaHeading.className = 'lexia-subsection-heading';
    personaHeading.textContent = 'Persona';
    root.insertBefore(personaHeading, personaOneTitle);
    makePersona(root, personaOneTitle, personaOneTitle.nextElementSibling, 'Persona 1');
    makePersona(root, personaTwoTitle, personaTwoTitle.nextElementSibling, 'Persona 2');

    const items = [];
    let cursor = experienceTitle.nextElementSibling;
    while (cursor && items.length < 5) {
      const next = cursor.nextElementSibling;
      items.push(cursor);
      cursor = next;
    }
    const [discover, treatment, givingUp, solution, map] = items;
    const experience = document.createElement('section');
    experience.className = 'lexia-experience';
    root.insertBefore(experience, experienceTitle);
    experienceTitle.textContent = 'Experience Mapping';
    experienceTitle.className = 'lexia-subsection-heading';
    const subtitle = document.createElement('p');
    subtitle.className = 'lexia-experience-subtitle';
    subtitle.textContent = "Parents' Point of View";
    map.classList.add('lexia-experience-map');
    const stageGrid = document.createElement('div');
    stageGrid.className = 'lexia-stage-grid';
    [[discover, 'Discover'], [treatment, 'Treatment'], [givingUp, 'Giving Up']].forEach(([copy, label]) => {
      const article = document.createElement('article');
      const title = document.createElement('h4');
      title.textContent = label;
      if (label === 'Treatment') {
        copy.remove();
        const intro = document.createElement('p');
        intro.textContent = 'A specialist confirms that the patient has dyslexia.';
        const list = document.createElement('ul');
        ['Start the dyslexia therapy program.', 'Visit once or twice a week and work with language therapists.', 'Therapists give homework to encourage steady learning.', 'Homework is often left undone.', 'The symptoms may begin to improve.'].forEach(text => {
          const item = document.createElement('li');
          item.textContent = text;
          list.append(item);
        });
        article.append(title, intro, list);
      } else {
        copy.querySelector('b')?.remove();
        copy.innerHTML = copy.innerHTML.replace(/^:\s*/, '');
        article.append(title, copy);
      }
      stageGrid.append(article);
    });
    const solutionBand = document.createElement('div');
    solutionBand.className = 'lexia-solution-band';
    solutionBand.innerHTML = '<article><h4>Solution Point</h4><p>If users suspect dyslexia, they can use the Diagnostic function in the app to receive guidance on whether to visit a specialized institution for a diagnosis.</p></article><article class="lexia-solution-wide"><h4>Solution Point</h4><p>With the application, children can continue learning Korean at their own pace when they are not attending classes at the institution. Exciting content in the app encourages children to study with their parents without a teacher. The application also provides parents with guidance on how to support their children. If the parents are too busy to teach, children can study by themselves.</p></article>';
    solution.remove();
    experience.append(experienceTitle, subtitle, map, stageGrid, solutionBand);
  }

  function enhanceInsights() {
    const root = section('s6');
    if (!root || root.dataset.layoutEnhanced) return;
    root.dataset.layoutEnhanced = 'true';
    const heroImage = image(root, 'lex_di_1');
    const quote = root.querySelector(':scope > .pull-quote');
    const hero = document.createElement('div');
    hero.className = 'lexia-insight-hero';
    hero.append(heroImage, quote);
    root.querySelector(':scope > h2').after(hero);

    const concept = heading(root, 'Concept');
    const conceptCopy = concept.nextElementSibling;
    const composition = root.querySelector('.compose');
    const digital = root.querySelector('.arrow-row');
    composition.classList.add('lexia-concept-composition');
    digital.classList.add('lexia-digital-concept');
    concept.after(composition);
    composition.after(conceptCopy);
    conceptCopy.after(digital);
    const digitalStart = conceptCopy.textContent.indexOf('We transformed');
    if (digitalStart > 0) {
      const digitalCopy = document.createElement('p');
      digitalCopy.textContent = conceptCopy.textContent.slice(digitalStart).trim();
      conceptCopy.textContent = conceptCopy.textContent.slice(0, digitalStart).trim();
      digital.after(digitalCopy);
    }
    [...root.querySelectorAll(':scope > .caption')]
      .find(el => el.textContent.startsWith('Combining the book'))?.remove();

    const multi = heading(root, '1. Multisensory');
    const story = heading(root, '2. Storytelling');
    const personal = heading(root, '3. Personalized');
    const game = heading(root, '4. Gamification');
    const multiCopy = multi.nextElementSibling;
    const storyCopy = story.nextElementSibling;
    const personalCopy = personal.nextElementSibling;
    const gameCopy = game.nextElementSibling;
    const multiImage = image(root, 'lex_di_7');
    const storyImage = image(root, 'lex_di_8');
    multiImage.alt = 'Multisensory instruction using letter blocks';
    storyImage.alt = 'Storytelling environment inspired by Alice in Wonderland';
    multi.after(multiImage);
    multiImage.after(multiCopy);
    story.after(storyImage);
    storyImage.after(storyCopy);
    const originalGrid = image(root, 'lex_di_9').parentElement;
    const personalGrid = document.createElement('div');
    const gameGrid = document.createElement('div');
    personalGrid.className = 'lexia-insight-pair';
    gameGrid.className = 'lexia-insight-pair';
    personalGrid.append(image(root, 'lex_di_9'), image(root, 'lex_di_10'));
    gameGrid.append(image(root, 'lex_di_11'), image(root, 'lex_di_12'));
    originalGrid.remove();
    personal.after(personalGrid);
    personalGrid.after(personalCopy);
    game.after(gameGrid);
    gameGrid.after(gameCopy);
  }

  function prototypeFigure(img, captionText) {
    const figure = document.createElement('figure');
    const caption = document.createElement('figcaption');
    caption.textContent = captionText;
    figure.append(img, caption);
    return figure;
  }

  function enhancePrototype() {
    const root = section('s7');
    if (!root || root.querySelector('.lexia-prototype-grid')) return;
    const labels = ['Diagnosis', 'Learning Phonics', 'Phonics Game', 'Understanding Phonemes', 'Report'];
    const blocks = labels.map(label => {
      const title = heading(root, label);
      return { title, copy: title.nextElementSibling };
    });
    blocks[0].copy.textContent = 'The app diagnoses dyslexia by assessing how well children understand the principles of consonants and vowels. Based on the results, it assesses their level of fluency.';
    blocks[1].copy.textContent = 'Using multimedia content, children learn how to pronounce letters.';
    blocks[2].copy.textContent = 'Based on the phonics that children have learned, they play a phonics game.';
    blocks[3].copy.textContent = 'Children learn how phonemes are pronounced when they are next to each other.';
    blocks[4].copy.textContent = 'The child and their parents receive a report based on the play session.';
    const grid = document.createElement('div');
    grid.className = 'lexia-prototype-grid';
    const makeCopy = (...indexes) => {
      const copy = document.createElement('div');
      copy.className = 'lexia-prototype-copy';
      indexes.forEach(index => copy.append(blocks[index].title, blocks[index].copy));
      return copy;
    };
    const rows = [
      [makeCopy(0), prototypeFigure(image(root, 'lex_lp_1'), 'The app guides children to replace consonants or vowels based on what they hear.'), prototypeFigure(image(root, 'lex_lp_2'), 'Children record themselves reading within a set time so the app can measure fluency.')],
      [makeCopy(1, 2), prototypeFigure(image(root, 'lex_lp_5'), 'Mouth and tongue movements show how each consonant and vowel is pronounced.'), prototypeFigure(image(root, 'lex_lp_6'), 'Children listen to vowels and select the answers in the correct order.')],
      [makeCopy(3, 4), prototypeFigure(image(root, 'lex_lp_3'), 'Combining letter blocks demonstrates how adjacent phonemes are pronounced.'), prototypeFigure(image(root, 'lex_lp_4'), 'Progress graphs and feedback guide both the child and their parents.')]
    ];
    rows.forEach(cells => {
      const row = document.createElement('div');
      row.className = 'lexia-prototype-row';
      row.append(...cells);
      grid.append(row);
    });
    [...root.children].slice(1).forEach(child => child.remove());
    root.append(grid);
  }

  function enhanceTesting() {
    const root = section('s8');
    if (!root || root.dataset.layoutEnhanced) return;
    root.dataset.layoutEnhanced = 'true';
    const wizard = heading(root, 'Wizard of Oz');
    const wizardCopy = wizard.nextElementSibling;
    const wizardLeft = image(root, 'lex_td_1');
    const wizardRight = image(root, 'lex_td_2');
    const wizardGrid = wizardLeft.parentElement;
    const oldCaption = wizardGrid.nextElementSibling;
    wizardGrid.className = 'lexia-test-pair';
    wizardGrid.innerHTML = '';
    wizardGrid.append(
      prototypeFigure(wizardLeft, 'Learning pronunciation with the parent using a book'),
      Object.assign(document.createElement('span'), { className: 'lexia-pair-arrow', textContent: '→' }),
      prototypeFigure(wizardRight, 'Ji-Yoon uses the application to learn Korean vowels on her own')
    );
    oldCaption.remove();
    wizard.after(wizardGrid);
    wizardGrid.after(wizardCopy);

    const expert = heading(root, 'Expert Interview');
    const expertQuote = expert.nextElementSibling;
    const expertCopy = expertQuote.nextElementSibling;
    const expertImage = image(root, 'lex_td_3');
    const nonwords = expertImage.nextElementSibling;
    const comments = nonwords.nextElementSibling;
    const expertGrid = document.createElement('div');
    expertGrid.className = 'lexia-expert-grid';
    expertQuote.innerHTML = '<span>“Instead of regular words, dyslexic children should practice non-words”</span><small>Dr. Jae-Seok Jung<br>Dyslexia expert and author of ‘Reading Confidence’</small>';
    expertGrid.append(expertImage, expertQuote);
    expert.after(expertGrid);
    expertGrid.after(expertCopy);
    comments.className = 'lexia-expert-comments';
    expertCopy.after(comments);
    const nonwordCard = document.createElement('div');
    nonwordCard.className = 'lexia-nonwords';
    nonwordCard.innerHTML = '<div class="lexia-nonwords-title">What Are Non-words?</div><p>A non-word is a combination of letters that has no meaning.</p><div class="lexia-word-pairs"><div><b>Regular words</b><span>Cat</span><span>Museum</span></div><div><b>Non-words</b><span>Caet</span><span>Mooseum</span></div></div>';
    nonwords.remove();
    comments.after(nonwordCard);

    const prototype = heading(root, 'Developing the Prototype');
    const prototypeCopy = prototype.nextElementSibling;
    const citation = prototypeCopy.nextElementSibling;
    const prototypeGrid = image(root, 'lex_td_4').parentElement;
    prototypeGrid.className = 'lexia-development-pair';
    prototype.after(prototypeGrid);
    prototypeGrid.after(prototypeCopy);
    prototypeCopy.after(citation);
  }

  enhanceBackground();
  enhanceProblems();
  enhanceDyslexia();
  enhanceResearch();
  enhanceInsights();
  enhancePrototype();
  enhanceTesting();
})();
