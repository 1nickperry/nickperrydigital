import fs from "fs";
import path from "path";

const TEXT_EXT = new Set([
  ".html",
  ".css",
  ".js",
  ".mjs",
  ".json",
  ".md",
  ".yml",
  ".yaml",
  ".svg",
  ".txt",
  ".xml",
]);

const SKIP_DIRS = new Set(["node_modules", ".git", ".decap-server"]);

function walk(dir, files = []) {
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    if (SKIP_DIRS.has(entry.name)) continue;
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) walk(full, files);
    else files.push(full);
  }
  return files;
}

export function checkSite(root = process.cwd()) {
  const errors = [];
  const files = walk(root);
  const banned = [
    ["em dash", "\u2014"],
    ["en dash", "\u2013"],
    ["horizontal bar", "\u2015"],
    ["emdash entity", "&" + "mdash;"],
    ["endash entity", "&" + "ndash;"],
    ["competitor brand", "Chuck" + "walla"],
    ["competitor brand lower", "chuck" + "walla"],
  ];

  for (const file of files) {
    const ext = path.extname(file);
    if (!TEXT_EXT.has(ext)) continue;
    const text = fs.readFileSync(file, "utf8");
    for (const [label, token] of banned) {
      if (text.includes(token)) {
        errors.push(`${path.relative(root, file)} contains ${label}`);
      }
    }
  }

  const required = [
    "index.html",
    "about/index.html",
    "pricing/index.html",
    "results/index.html",
    "services/index.html",
    "services/ai-search-optimization/index.html",
    "contact/index.html",
    "locations/index.html",
    "locations/grand-junction/index.html",
    "locations/durango/index.html",
    "blog/index.html",
    "privacy/index.html",
    "terms/index.html",
    "sitemap.xml",
    "robots.txt",
    "assets/css/site.css",
    "admin/index.html",
    "admin/config.yml",
  ];
  for (const rel of required) {
    if (!fs.existsSync(path.join(root, rel))) errors.push(`Missing ${rel}`);
  }

  const home = fs.readFileSync(path.join(root, "index.html"), "utf8");
  for (const token of [
    "Book a Free Strategy Call",
    "ProfessionalService",
    "555-010-0190",
    "Ready to Grow?",
    "Areas We Serve",
    "$1,000",
    "$850",
    "$1,500",
    "$150",
  ]) {
    if (!home.includes(token)) errors.push(`Home missing ${token}`);
  }
  const nav = home.split("<main")[0];
  const labels = ["About", "Pricing", "Results", "Services", "Contact"];
  let last = -1;
  for (const label of labels) {
    const at = nav.indexOf(`>${label}<`);
    if (at < 0 || at < last) errors.push(`Nav order problem at ${label}`);
    last = at;
  }

  const fruita = fs.readFileSync(path.join(root, "locations/fruita/index.html"), "utf8");
  if (!fruita.includes("FAQPage")) errors.push("Fruita page missing FAQPage schema");
  if (!fruita.includes("What it costs in Fruita")) errors.push("Fruita page missing cost section");

  const contact = fs.readFileSync(path.join(root, "contact/index.html"), "utf8");
  if (!contact.includes("<form")) errors.push("Contact missing form");
  if (!contact.toLowerCase().includes("placeholder")) errors.push("Contact missing placeholder mark");
  if (!contact.includes('id="booking"')) errors.push("Contact missing booking block");

  const study = fs.readFileSync(
    path.join(root, "case-studies/placeholder-contractor/index.html"),
    "utf8"
  );
  if (!study.includes("Placeholder")) errors.push("Case study missing placeholder label");

  const htmlFiles = files.filter((file) => file.endsWith(".html") && !file.includes(`${path.sep}admin${path.sep}`));
  for (const file of htmlFiles) {
    const html = fs.readFileSync(file, "utf8");
    const hrefs = [...html.matchAll(/href="(\/[^"]*)"/g)].map((match) => match[1]);
    for (const href of hrefs) {
      if (href.startsWith("/admin")) continue;
      const [pathname, hash] = href.split("#");
      if (!pathname || pathname === "/") continue;
      const rel = pathname.endsWith("/")
        ? `${pathname.slice(1)}index.html`
        : pathname.slice(1);
      if (!fs.existsSync(path.join(root, rel))) {
        errors.push(`${path.relative(root, file)} links to missing ${href}`);
      }
      void hash;
    }
  }

  if (errors.length) {
    console.error(errors.join("\n"));
    throw new Error(`Site check failed with ${errors.length} problem(s)`);
  }
  console.log("Site check passed");
}

if (process.argv[1] && process.argv[1].endsWith("check.mjs")) {
  checkSite(path.resolve(path.dirname(new URL(import.meta.url).pathname), ".."));
}
