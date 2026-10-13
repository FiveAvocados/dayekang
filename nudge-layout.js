(function () {
  const body = document.body;
  if (!body.classList.contains('nudge-page')) return;

  const asset = (name) => `assets/optimized/${name}.webp?v=20261013-nudge-layout`;
  const img = (name, alt, className = '') =>
    `<img${className ? ` class="${className}"` : ''} src="${asset(name)}" alt="${alt}" loading="lazy">`;

  const service = document.getElementById('s2');
  if (service) {
    service.innerHTML = `
      <h2 class="reveal">Service Summary</h2>
      <div class="nudge-service-grid">
        <div class="nudge-service-visual">
          ${img('nud_ss_1', 'A hospitalized child walking through a long hospital hallway')}
        </div>
        <article class="nudge-service-reality">
          <h3>Reality</h3>
          <p>Lack of physical activity can cause stress and slow recovery for hospitalized children. However, even though children want to walk, there are no suitable trails that they can enjoy every day.</p>
        </article>
        <blockquote class="nudge-service-quote">“Why are there no children playing at a children's hospital?”</blockquote>
        <article class="nudge-service-problem">
          <h3>Problem</h3>
          <p>Currently, children can use outdoor trails or an indoor hallway for walking. The outdoor trails are easily affected by the weather. Fine dust also prevents children from using them as often as needed. The indoor hallway is dull and boring, so the children do not enjoy walking there. Because a lack of physical activity can slow recovery and cause stress, it is important to ensure that children can take a walk every day.</p>
        </article>
        <div class="nudge-service-answer">
          <article>
            <h3>Solution</h3>
            <p>By providing a safe and fun trail design, we can help children relieve stress from the daily treatment process. Considering the hospital's budget constraints, we created a nudge design in the hallway to make walking more engaging. Characters and stories on the wall can motivate hospitalized children to take walks every day.</p>
          </article>
          <article>
            <h3>Importance</h3>
            <p>This solution can provide a positive hospital experience for children, and it can help them recover more quickly.</p>
          </article>
        </div>
      </div>`;
  }

  const research = document.getElementById('s3');
  if (research) {
    research.innerHTML = `
      <h2 class="reveal">Research Process</h2>

      <section class="nudge-research-block nudge-desk-research">
        <h3>Desk Research</h3>
        <div class="nudge-desk-grid">
          <div class="nudge-desk-collage">
            ${img('nud_rp_1', 'Social-media post showing a hospitalized child walking')}
            ${img('nud_rp_2', 'Social-media post showing a hospitalized child eating in bed')}
          </div>
          <div class="nudge-desk-copy">
            <article>
              <h4>Online Research</h4>
              <p>We observed posts on social networks such as Instagram, blogs, and internet cafes to understand physical activity and entertainment in children's hospitals.</p>
            </article>
            <article>
              <h4>Daily life spent in bed all day</h4>
              <p>The hospital is a shared space, so people avoid letting their children play noisy games. A guardian may give a child a smartphone because the child likes watching videos with a headset, and it is relatively quiet. Due to concerns about spreading infections, it is not easy to meet friends in the hospital.</p>
            </article>
          </div>
        </div>
      </section>

      <section class="nudge-research-block nudge-field-observation">
        <h3>Field Research</h3>
        <article class="nudge-survey-copy">
          <h4>A quantitative survey of hospital movements</h4>
          <p>We surveyed thirty-two children for four days, and the survey showed that they moved for no more than 20 minutes in the hospital. According to the paper, children need to walk 12,000–15,000 steps for their physical health, but the hospitalized children did not take more than 2,000 steps.</p>
          <p class="caption">* About 110 steps per minute for a walk, 140 steps for a fast walk, and 180 steps for jogging.</p>
        </article>
        <article class="nudge-observation-copy">
          <h4>Observation</h4>
          <p>We visited children's hospitals, including Asan Medical Center, Severance Hospital, and Seoul National University Hospital, where we observed and interviewed nurses and hospitalized children.</p>
        </article>
        <div class="nudge-observation-media">
          <figure><div class="nudge-observation-frame">${img('nud_rp_3', "Outdoor trail at a children's hospital")}</div><figcaption>Outdoor trails</figcaption></figure>
          <figure><div class="nudge-observation-frame">${img('nud_rp_4', 'Indoor walking-distance markings in a hospital hallway')}</div><figcaption>Indoor installation</figcaption></figure>
        </div>
      </section>

      <section class="nudge-child-interview">
        <div class="nudge-child-identity">
          <div><strong>Hey-Jin Kim</strong><span>10 years old</span></div>
          ${img('nud_rp_7', 'Hey-Jin Kim, a ten-year-old hospitalized child')}
        </div>
        <div class="nudge-child-copy">
          <h3>Interview with a child from<br>Seoul National University Children's Hospital</h3>
          <p>When we found that she was not bringing all of her things from the refrigerator to her bed at once, we asked her why.</p>
          <p>“I intentionally do not bring all the food that I need at once because it forces me to walk more. My doctor always says I have to work out when I'm in the hospital.”</p>
        </div>
      </section>

      <section class="nudge-research-block nudge-asan-research">
        <h3>Field Research</h3>
        <div class="nudge-asan-media">
          <div class="nudge-asan-primary">${img('nud_rp_5', 'Interview participant at the Asan Design Innovation Center')}</div>
          <figure>${img('nud_rp_8', 'Interview at the Asan Design Innovation Center')}<figcaption>Asan Design Innovation Center</figcaption></figure>
          <figure>${img('nud_rp_6', "A nurse working at the children's hospital")}<figcaption>A nurse working at the children's hospital</figcaption></figure>
        </div>
        <div class="nudge-asan-copy">
          <p>We interviewed staff at the Asan Medical Design Innovation Center about children's physical activities. Asan Children's Hospital had no play space for children, and there was little awareness of their physical activity. Regarding children's physical activity, a nurse mentioned that walking was enough. The nurse at Asan Children's Hospital said, “Since children cannot exercise vigorously in a hospital, walking can be enough.”</p>
          <blockquote>“Walking is a great exercise for hospitalized children.”</blockquote>
        </div>
      </section>

      <section class="nudge-research-block nudge-affinity">
        <h3>Affinity Diagram</h3>
        <div class="nudge-affinity-media">
          ${img('nud_rp_9', 'Affinity diagram cards being arranged on a table')}
          ${img('nud_rp_10b', 'Affinity diagram notes being arranged on a wall')}
        </div>
        <p>Based on the affinity diagram, we developed three insights from the stakeholders' viewpoints.</p>
        <div class="nudge-stakeholder-insights">
          <article><h4>Hospitalized children</h4><p>They cannot move easily because of IV poles.<br>The space does not feel like a play area because of adult control.</p></article>
          <article><h4>Parents</h4><p>When children play in the hallway, it's easy to observe children's activities and seek medical attention in case of a problem. However, parents were concerned about obstructing the hallway for other patients and clinicians.</p></article>
          <article><h4>Hospital</h4><p>The hallway is suitable for walking because it does not require extra space. However, nurses are concerned that if children move around without order, there will be problems with medical care and treatment.</p></article>
        </div>
      </section>`;
  }

  const insights = document.getElementById('s4');
  if (insights) {
    insights.innerHTML = `
      <h2 class="reveal">Design Insights</h2>
      <div class="nudge-insight-quote">
        <blockquote>“Let's make the hallway a place for the children to play safely”</blockquote>
        <svg viewBox="0 0 260 150" role="img" aria-label="Playful sneaker illustration">
          <path d="M28 86c21-4 36-15 55-35 8-9 20-9 28 0l22 28c17 21 34 25 69 24 23-1 36 9 36 24 0 13-12 19-31 19H48c-22 0-35-10-35-27 0-15 5-29 15-33Z" fill="#ef8fc5" stroke="#111" stroke-width="5" stroke-linejoin="round"/>
          <path d="M16 119c31 9 166 7 219 1l3 17c-55 10-175 12-215 4-9-2-13-10-7-22Z" fill="#66b8e8" stroke="#111" stroke-width="5"/>
          <path d="M68 76l29 24m-13-37l31 25m-6-31l27 27" fill="none" stroke="#111" stroke-width="5" stroke-linecap="round"/>
          <circle cx="192" cy="116" r="7" fill="#f6e75a" stroke="#111" stroke-width="4"/>
        </svg>
      </div>
      <section class="nudge-definition">
        <h3>Nudge Design</h3>
        ${img('nud_di_1', 'Nudge design in Amsterdam uses red lines to guide people toward stairs')}
        <div class="nudge-definition-copy">
          <article><h4>Nudge Design</h4><p>Nudge is a concept in behavioral science, political theory, and economics that proposes positive reinforcement and indirect suggestions to influence the behavior and decision-making of groups or individuals.</p></article>
          <article><h4>Nudge Design in Amsterdam</h4><p>It used red lines to suggest that visitors use the stairs rather than the lifts.</p></article>
        </div>
      </section>`;
  }

  const prototype = document.getElementById('s5');
  if (prototype) {
    prototype.innerHTML = `
      <h2 class="reveal">Prototype &amp; Testing</h2>
      <section class="nudge-prototype-block nudge-prototype-one">
        <h3>Prototype 1</h3>
        <div class="nudge-prototype-one-grid">
          ${img('nud_pt_1', 'Making a maze prototype with footprints')}
          <article><h4>Making a maze prototype with footprints</h4><p>We used a maze, symbols, and footprints to induce children to walk and stretch their legs.</p></article>
        </div>
      </section>
      <section class="nudge-prototype-block nudge-prototype-one-test">
        <h3>Prototype 1 Testing</h3>
        <div class="nudge-prototype-test-grid">
          ${img('nud_pt_2', 'Children walking on the maze prototype and sharing feedback')}
          <article><h4>Prototype Testing at Kyeongdong Elementary School</h4><p>We introduced the prototype to the children, who walked on it by following the lines, symbols, and footprints. After the test, we received feedback from the children. They wanted more complex missions and opportunities to play with friends.</p></article>
          <p class="caption">Children walking on the prototype<br><br>Children gave feedback about the prototype</p>
        </div>
      </section>
      <section class="nudge-prototype-block nudge-prototype-two">
        <h3>Prototype 2</h3>
        <p>We added wallpapers to encourage various stretches. By adding a story to the wallpaper, children can also enjoy the story while they walk. The story is about a bird that gets sick and becomes healthy again with the help of its friends.</p>
        <figure>${img('nud_pt_3', 'Bird-story wallpaper for neck stretches')}<figcaption><strong>Neck stretch</strong><br>Follow the birds trying to fly again! The child can naturally stretch their neck while following the birds in sequence.</figcaption></figure>
        <figure>${img('nud_pt_4', 'Animal characters demonstrating different types of steps')}<figcaption><strong>Different types of steps</strong><br>Children can follow the movements of animals and try different types of steps.</figcaption></figure>
      </section>
      <section class="nudge-prototype-block nudge-prototype-two-test">
        <h3>Prototype 2 Testing</h3>
        <div class="nudge-usability-grid">
          ${img('nud_pt_5', 'Hyeon-Min trying the story wallpaper and adjusting a footprint', 'nudge-usability-main')}
          ${img('nud_pt_6', 'Hyeon-Min walking the trail while pulling a suitcase', 'nudge-usability-side')}
          <article><h4>Usability test</h4><p>We tested the prototype with Hyeon-Min, and she enjoyed following the footprints. We asked her to carry a suitcase because we wanted to mimic the walking experience with an IV pole. She was able to walk the whole trail without difficulty. When she had a chance to modify the game, she participated actively and suggested different, interesting footsteps.</p></article>
        </div>
      </section>`;
  }

  const outcome = document.getElementById('s6');
  if (outcome) {
    outcome.innerHTML = `
      <h2 class="reveal">Outcome &amp; Effects</h2>
      ${img('nud_hero', "Final nudge design installed in a children's hospital hallway", 'nudge-outcome-image')}
      <div class="nudge-outcome-copy">
        <article><h3>Hospitalized children</h3><p>The aesthetically pleasing and playful wall prints can reduce negative images of hospitals. Through physical activity, children can improve their mental health and recover faster.</p></article>
        <article><h3>Parents</h3><p>They are relieved because the prints act as a guideline. The child can safely play with the design. It may reduce the risk of secondary infections and accidents.</p></article>
        <article><h3>Hospital</h3><p>The children walk the corridor in an orderly fashion, so there is no disruption to their work.</p></article>
      </div>`;
  }
})();
