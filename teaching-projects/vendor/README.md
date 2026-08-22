# Local visualization libraries

The student visualization pages use these checked-in browser libraries so the
projects keep working when an external CDN or internet connection is unavailable.

- `d3.v7.9.0.min.js`
  - Source: https://d3js.org/d3.v7.min.js
  - SHA-256: `f2094bbf6141b359722c4fe454eb6c4b0f0e42cc10cc7af921fc158fceb86539`
- `topojson.v3.0.2.min.js`
  - Source: https://d3js.org/topojson.v3.min.js
  - SHA-256: `b47a003c6a0d761211dbc60797d0d62f37917ddc228241fb38205732b1d78683`

Do not replace these files or restore CDN script tags without updating and running
`node teaching-projects/validate-projects.mjs`.
