import http from "http";
import fs from "fs";
import path from "path";
import { projectRoot } from "./content.mjs";

const root = projectRoot();
const port = Number(process.env.PORT || 4173);
const types = {
  ".html": "text/html; charset=utf-8",
  ".css": "text/css; charset=utf-8",
  ".js": "text/javascript; charset=utf-8",
  ".mjs": "text/javascript; charset=utf-8",
  ".json": "application/json; charset=utf-8",
  ".svg": "image/svg+xml",
  ".png": "image/png",
  ".webp": "image/webp",
  ".xml": "application/xml; charset=utf-8",
  ".txt": "text/plain; charset=utf-8",
  ".yml": "text/yaml; charset=utf-8",
  ".ico": "image/x-icon",
};

function resolveFile(urlPath) {
  const clean = decodeURIComponent(urlPath.split("?")[0]);
  const rel = clean.endsWith("/") ? `${clean}index.html` : clean;
  const file = path.normalize(path.join(root, rel));
  if (!file.startsWith(root)) return null;
  return file;
}

const server = http.createServer((req, res) => {
  const file = resolveFile(req.url || "/");
  let status = 200;
  let target = file;
  if (!target || !fs.existsSync(target) || fs.statSync(target).isDirectory()) {
    target = path.join(root, "404.html");
    status = 404;
  }
  if (!fs.existsSync(target)) {
    res.writeHead(404, { "Content-Type": "text/plain; charset=utf-8" });
    res.end("Not found");
    return;
  }
  const ext = path.extname(target);
  res.writeHead(status, { "Content-Type": types[ext] || "application/octet-stream" });
  fs.createReadStream(target).pipe(res);
});

server.listen(port, () => {
  console.log(`Nick Perry Digital site at http://localhost:${port}`);
});
