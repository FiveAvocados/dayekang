import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const toolDir = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(toolDir, '..');

const assets = [
  {
    source: path.join(root, 'teaching-projects/natural-disaster-mortality/countries-110m.json'),
    output: path.join(root, 'assets/toonnote-covid-world-110m.js'),
    global: 'TOONNOTE_COVID_WORLD_110M',
  },
  {
    source: path.join(root, 'assets/toonnote-us-states-10m.json'),
    output: path.join(root, 'assets/toonnote-us-states-10m.js'),
    global: 'TOONNOTE_US_STATES_10M',
  },
  {
    source: path.join(root, 'assets/toonnote-covid-study-data.json'),
    output: path.join(root, 'assets/toonnote-covid-study-data.js'),
    global: 'TOONNOTE_COVID_STUDY_DATA',
  },
];

for (const asset of assets) {
  const json = JSON.parse(fs.readFileSync(asset.source, 'utf8'));
  const payload = `window.${asset.global}=${JSON.stringify(json)};\n`;
  fs.writeFileSync(asset.output, payload, 'utf8');
  console.log(`${path.relative(root, asset.output)} <- ${path.relative(root, asset.source)}`);
}
