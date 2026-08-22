import { createHash } from "node:crypto";
import { readFileSync, statSync } from "node:fs";
import { dirname, extname, join } from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";
import { runInNewContext } from "node:vm";
import { offlineProjects, renderOfflineBundle } from "./build-offline-data.mjs";

const projectRoot = dirname(fileURLToPath(import.meta.url));

const vendorFiles = [
  {
    path: "vendor/d3.v7.9.0.min.js",
    sha256: "f2094bbf6141b359722c4fe454eb6c4b0f0e42cc10cc7af921fc158fceb86539"
  },
  {
    path: "vendor/topojson.v3.0.2.min.js",
    sha256: "b47a003c6a0d761211dbc60797d0d62f37917ddc228241fb38205732b1d78683"
  }
];

const projects = [
  {
    name: "NBA Legends",
    page: "nba-legends/index.html",
    required: [
      "nba-legends/datasets/advanced_stats.csv",
      "nba-legends/datasets/per_game_stats.csv",
      "nba-legends/datasets/salaries.csv",
      "nba-legends/datasets/jordanmeme.png"
    ]
  },
  {
    name: "Natural Disaster Mortality",
    page: "natural-disaster-mortality/index.html",
    topojson: true,
    required: [
      "natural-disaster-mortality/countries-110m.json",
      "natural-disaster-mortality/natural-disasters.csv",
      "natural-disaster-mortality/earthquake.csv",
      "natural-disaster-mortality/hurricane.csv",
      "natural-disaster-mortality/motorVehicle.csv",
      "natural-disaster-mortality/heart.csv",
      "natural-disaster-mortality/cancer.csv",
      "natural-disaster-mortality/suicide.csv"
    ]
  },
  {
    name: "Streaming Catalogs",
    page: "streaming-catalogs/index.html",
    required: [
      "streaming-catalogs/datasets/clean/disney.csv",
      "streaming-catalogs/datasets/clean/netflix.csv"
    ]
  },
  {
    name: "US Cost of Living",
    page: "us-cost-of-living/index.html",
    topojson: true,
    required: [
      "us-cost-of-living/us-smaller.json",
      "us-cost-of-living/monthly_income.csv"
    ]
  },
  {
    name: "Global Inequality and Emissions",
    page: "global-inequality-emissions/index.html",
    topojson: true,
    required: [
      "global-inequality-emissions/data/countries_clean.json",
      "global-inequality-emissions/data/slim-3.json",
      "global-inequality-emissions/data/gdp.json",
      "global-inequality-emissions/data/gini.json",
      "global-inequality-emissions/data/co2.json",
      "global-inequality-emissions/data/sector_emissions.json"
    ]
  }
];

const failures = [];

const fail = (message) => failures.push(message);
const load = (relativePath) => readFileSync(join(projectRoot, relativePath));

for (const vendor of vendorFiles) {
  try {
    const digest = createHash("sha256").update(load(vendor.path)).digest("hex");
    if (digest !== vendor.sha256) fail(`${vendor.path}: checksum changed`);
  } catch (error) {
    fail(`${vendor.path}: ${error.message}`);
  }
}

for (const project of projects) {
  let html = "";
  try {
    html = load(project.page).toString("utf8");
  } catch (error) {
    fail(`${project.name}: missing ${project.page}`);
    continue;
  }

  if (!html.includes("../vendor/d3.v7.9.0.min.js")) {
    fail(`${project.name}: local D3 script is not linked`);
  }
  if (project.topojson && !html.includes("../vendor/topojson.v3.0.2.min.js")) {
    fail(`${project.name}: local TopoJSON script is not linked`);
  }
  if (/d3js\.org|cdnjs\.cloudflare\.com\/.*highlight|topojson\.v3\.min\.js/.test(html.replaceAll("../vendor/topojson.v3.0.2.min.js", ""))) {
    fail(`${project.name}: external visualization dependency found`);
  }
  if (!html.includes("../responsive-project.js") || !html.includes("../responsive-project.css")) {
    fail(`${project.name}: responsive compatibility layer is missing`);
  }
  if (!html.includes('window.location.protocol === "file:"') || !html.includes("offline-data.js")) {
    fail(`${project.name}: local-file data compatibility layer is missing`);
  }

  for (const relativePath of project.required) {
    const absolutePath = join(projectRoot, relativePath);
    try {
      if (statSync(absolutePath).size === 0) {
        fail(`${project.name}: ${relativePath} is empty`);
        continue;
      }

      const extension = extname(relativePath).toLowerCase();
      const contents = readFileSync(absolutePath, "utf8");
      if (extension === ".json") JSON.parse(contents);
      if (extension === ".csv") {
        const rows = contents.split(/\r?\n/).filter((row) => row.trim().length > 0);
        if (rows.length < 2 || !rows[0].includes(",")) {
          fail(`${project.name}: ${relativePath} has no usable CSV data`);
        }
      }
    } catch (error) {
      fail(`${project.name}: ${relativePath} cannot be read (${error.message})`);
    }
  }
}

for (const project of offlineProjects) {
  const bundlePath = join(project.directory, "offline-data.js");
  try {
    const actual = load(bundlePath).toString("utf8");
    const expected = renderOfflineBundle(project);
    if (actual !== expected) {
      fail(`${project.name}: ${bundlePath} is stale; run node teaching-projects/build-offline-data.mjs`);
      continue;
    }

    const pageUrl = pathToFileURL(join(projectRoot, project.directory, "index.html"));
    const window = {
      location: pageUrl,
      fetch: async () => { throw new Error("unexpected native file fetch"); }
    };
    runInNewContext(actual, { window, URL, Response });

    for (const requestPath of project.files) {
      const response = await window.fetch(requestPath);
      const actualContents = await response.text();
      const expectedContents = load(join(project.directory, requestPath))
        .toString("utf8")
        .replace(/^\uFEFF/, "");
      if (!response.ok || actualContents !== expectedContents) {
        fail(`${project.name}: local-file fetch failed for ${requestPath}`);
      }
    }
  } catch (error) {
    fail(`${project.name}: ${bundlePath} cannot be checked (${error.message})`);
  }
}

if (failures.length > 0) {
  console.error("Student project validation failed:\n");
  failures.forEach((message) => console.error(`- ${message}`));
  process.exitCode = 1;
} else {
  console.log(`Validated ${projects.length} student visualization projects.`);
  console.log("Local libraries, data files, and responsive layers are intact.");
}
