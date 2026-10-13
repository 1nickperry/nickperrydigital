import fs from "fs";
import path from "path";
import { load as loadYaml } from "js-yaml";
import { marked } from "marked";

marked.use({
  async: false,
  gfm: true,
  breaks: false,
});

const root = path.resolve(path.dirname(new URL(import.meta.url).pathname), "..");

export function projectRoot() {
  return root;
}

export function readJson(rel) {
  return JSON.parse(fs.readFileSync(path.join(root, rel), "utf8"));
}

export function loadMarkdownFile(abs) {
  const raw = fs.readFileSync(abs, "utf8");
  const match = raw.match(/^---\r?\n([\s\S]*?)\r?\n---\r?\n([\s\S]*)$/);
  if (!match) {
    throw new Error(`Missing front matter: ${abs}`);
  }
  const data = loadYaml(match[1]) || {};
  const body = match[2].trim();
  return {
    ...data,
    body,
    html: marked.parse(body),
    slug: data.slug || path.basename(abs, path.extname(abs)),
  };
}

function loadDir(rel, ext) {
  const dir = path.join(root, rel);
  if (!fs.existsSync(dir)) return [];
  return fs
    .readdirSync(dir)
    .filter((name) => name.endsWith(ext))
    .map((name) => {
      const abs = path.join(dir, name);
      if (ext === ".json") {
        const data = JSON.parse(fs.readFileSync(abs, "utf8"));
        const slug = data.slug || path.basename(name, ext);
        const body = data.body || "";
        return { ...data, slug, html: body ? marked.parse(body) : "" };
      }
      return loadMarkdownFile(abs);
    })
    .filter((item) => !item.draft);
}

export function loadContent() {
  const settings = readJson("content/settings.json");
  const home = readJson("content/home.json");
  const services = loadDir("content/services", ".json").sort((a, b) => a.order - b.order);
  const locations = loadDir("content/locations", ".json").sort((a, b) => a.order - b.order);
  const caseStudies = loadDir("content/case-studies", ".json").sort((a, b) => a.order - b.order);
  const posts = loadDir("content/blog", ".md").sort((a, b) => String(b.date).localeCompare(String(a.date)));
  const pages = Object.fromEntries(
    loadDir("content/pages", ".md").map((page) => [page.slug, page])
  );

  const portraitPng = path.join(root, "assets/img/nick-perry.png");
  const portraitWebp = path.join(root, "assets/img/nick-perry.webp");

  return {
    settings,
    home,
    services,
    locations,
    caseStudies,
    posts,
    pages,
    hasPortrait: fs.existsSync(portraitPng),
    hasWebp: fs.existsSync(portraitWebp),
  };
}

export function md(src) {
  return marked.parse(src || "");
}
