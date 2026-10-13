import fs from "fs";
import path from "path";
import sharp from "sharp";
import { loadContent, projectRoot } from "./content.mjs";
import { renderRobots, renderSite, renderSitemap } from "./render.mjs";
import { checkSite } from "./check.mjs";

const root = projectRoot();

const GENERATED_DIRS = [
  "about",
  "pricing",
  "results",
  "services",
  "contact",
  "locations",
  "blog",
  "case-studies",
  "privacy",
  "terms",
];

function outputPath(route) {
  if (route === "/404.html") return "404.html";
  if (route === "/") return "index.html";
  return `${route.replace(/^\//, "").replace(/\/$/, "")}/index.html`;
}

async function preparePortrait() {
  const dir = path.join(root, "assets/img");
  fs.mkdirSync(dir, { recursive: true });
  const png = path.join(dir, "nick-perry.png");
  const candidates = [
    "/home/workdir/attachments/image.png",
    path.join(root, "uploads/me-but-stencil.png"),
  ];
  if (!fs.existsSync(png)) {
    for (const candidate of candidates) {
      if (fs.existsSync(candidate)) {
        fs.copyFileSync(candidate, png);
        console.log(`Copied portrait from ${candidate}`);
        break;
      }
    }
  }
  if (!fs.existsSync(png)) {
    console.warn("Portrait missing: assets/img/nick-perry.png");
    return;
  }
  const webp = path.join(dir, "nick-perry.webp");
  await sharp(png)
    .rotate()
    .resize({ width: 1200, withoutEnlargement: true })
    .webp({ quality: 74 })
    .toFile(webp);
  const pngStat = fs.statSync(png);
  const webpStat = fs.statSync(webp);
  console.log(`Portrait png ${pngStat.size} bytes, webp ${webpStat.size} bytes`);
}

function clean() {
  for (const dir of GENERATED_DIRS) {
    fs.rmSync(path.join(root, dir), { recursive: true, force: true });
  }
  for (const file of ["index.html", "404.html", "sitemap.xml", "robots.txt"]) {
    fs.rmSync(path.join(root, file), { force: true });
  }
}

async function main() {
  await preparePortrait();
  clean();
  const data = loadContent();
  const pages = renderSite(data);
  for (const page of pages) {
    const rel = outputPath(page.route);
    const abs = path.join(root, rel);
    fs.mkdirSync(path.dirname(abs), { recursive: true });
    fs.writeFileSync(abs, page.html);
  }
  const domain = data.settings.domain;
  fs.writeFileSync(path.join(root, "sitemap.xml"), renderSitemap(pages, domain));
  fs.writeFileSync(path.join(root, "robots.txt"), renderRobots(domain));
  console.log(`Wrote ${pages.length} pages`);
  checkSite(root);
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});
