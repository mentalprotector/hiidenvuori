import fs from "node:fs";
import path from "node:path";

const root = path.resolve("_site");
const siteOrigin = "https://xn--b1addkdc4ajs2ap.xn--p1ai";
const legacyPages = [
  "agreement.html", "aktivnyj-otdykh.html", "comment.html", "contacts.html",
  "konczertnye-programmy.html", "magazin-kafe-saha.html", "privacy.html",
  "razmeshhenie.html", "rules.html", "spusk-dlya-katerov.html",
  "stoyanka-dlya-avtodomov.html", "transfer-v-ruskealu.html", "uslugi.html"
];
const cleanRedirects = [...legacyPages.map((name) => name.replace(/\.html$/, "")), "palatki-na-nastilah"];
const publicPaths = [
  "/", "/agreement.html", "/comment.html", "/contacts.html",
  "/privacy.html", "/razmeshhenie.html",
  "/rules.html", "/spusk-dlya-katerov.html",
  "/uslugi.html"
];
const errors = [];
let renderedHtml = "";

function walk(directory) {
  return fs.readdirSync(directory, { withFileTypes: true }).flatMap((entry) => {
    const fullPath = path.join(directory, entry.name);
    return entry.isDirectory() ? walk(fullPath) : [fullPath];
  });
}

function requireFile(relativePath) {
  const fullPath = path.join(root, relativePath);
  if (!fs.existsSync(fullPath) || !fs.statSync(fullPath).isFile()) {
    errors.push(`Missing file: ${relativePath}`);
  }
}

function outputPathFromUrl(urlPath) {
  let pathname = decodeURI(urlPath.split("#", 1)[0].split("?", 1)[0]);
  if (pathname === "/") return path.join(root, "index.html");
  if (pathname.endsWith("/")) return path.join(root, pathname.slice(1), "index.html");
  return path.join(root, pathname.replace(/^\//, ""));
}

function checkReference(sourceFile, rawReference) {
  if (!rawReference || /^(?:#|mailto:|tel:|javascript:|data:)/i.test(rawReference)) return;

  let reference = rawReference;
  if (/^https?:\/\//i.test(reference)) {
    if (!reference.startsWith(siteOrigin)) return;
    reference = reference.slice(siteOrigin.length) || "/";
  } else if (/^\/\//.test(reference)) {
    return;
  }

  const cleanReference = reference.split("#", 1)[0].split("?", 1)[0];
  if (!cleanReference) return;
  if (sourceFile.endsWith(".css") && (cleanReference.includes("grid_12/") || /^(?:triggers-ft|icon-font)\.eot/i.test(cleanReference))) {
    const isFancyboxAsset = cleanReference.includes("/fancybox/");
    const isLegacyIconFont = cleanReference.includes("/fonts/triggers-ft-") || cleanReference.includes("/fonts/icon-font-") || /^(?:triggers-ft|icon-font)\.eot/i.test(cleanReference);
    const usesFancybox = /class=["'][^"']*fancybox/i.test(renderedHtml);
    const usesLegacyIconFont = /class=["'][^"']*(?:-triggers-ft|-icon-font)/i.test(renderedHtml);
    if ((isFancyboxAsset && !usesFancybox) || (isLegacyIconFont && !usesLegacyIconFont)) return;
  }
  const target = cleanReference.startsWith("/")
    ? outputPathFromUrl(cleanReference)
    : path.resolve(path.dirname(sourceFile), decodeURI(cleanReference));

  if (!fs.existsSync(target)) {
    errors.push(`Broken local reference in ${path.relative(root, sourceFile)}: ${rawReference}`);
  }
}

if (!fs.existsSync(root)) {
  console.error("Build directory _site does not exist. Run npm run build first.");
  process.exit(1);
}

legacyPages.forEach(requireFile);
cleanRedirects.forEach((slug) => requireFile(path.join(slug, "index.html")));
["404.html", "CNAME", ".nojekyll", "robots.txt", "sitemap.xml"].forEach(requireFile);

const files = walk(root);
renderedHtml = files
  .filter((file) => file.endsWith(".html"))
  .map((file) => fs.readFileSync(file, "utf8"))
  .join("\n");
for (const file of files) {
  if (!/\.(?:html|css)$/i.test(file)) continue;
  const source = fs.readFileSync(file, "utf8");
  const references = [
    ...source.matchAll(/(?:href|src|poster|data-src)=["']([^"']+)["']/gi),
    ...source.matchAll(/url\(\s*["']?([^"')]+)["']?\s*\)/gi)
  ];
  references.forEach((match) => checkReference(file, match[1]));
}

for (const publicPath of publicPaths) {
  const file = outputPathFromUrl(publicPath);
  const html = fs.readFileSync(file, "utf8");
  const expectedUrl = siteOrigin + publicPath;
  if (!html.includes(`<link href="${expectedUrl}" rel="canonical"`)) {
    errors.push(`Wrong canonical: ${publicPath}`);
  }
  if (!html.includes(`<meta content="${expectedUrl}" property="og:url"`)) {
    errors.push(`Wrong og:url: ${publicPath}`);
  }
}

const sitemap = fs.readFileSync(path.join(root, "sitemap.xml"), "utf8");
publicPaths.forEach((publicPath) => {
  if (!sitemap.includes(`<loc>${siteOrigin}${publicPath}</loc>`)) {
    errors.push(`Sitemap is missing: ${publicPath}`);
  }
});
cleanRedirects.forEach((slug) => {
  if (sitemap.includes(`${siteOrigin}/${slug}/`)) {
    errors.push(`Redirect leaked into sitemap: /${slug}/`);
  }
});

for (const obsoleteScript of ["jquery.min.js", "jquery-ui.min.js", "vendor-a7baa6bdbf.min.js", "bundle.js", "scripts-3457bd92a3.js", "translate.js"]) {
  if (renderedHtml.includes(obsoleteScript)) errors.push(`Obsolete script is still referenced: ${obsoleteScript}`);
}

if (errors.length) {
  console.error(errors.join("\n"));
  process.exit(1);
}

console.log(`Verified ${legacyPages.length} legacy HTML URLs, ${cleanRedirects.length} clean-URL redirects and ${files.length} build files.`);
console.log("Canonical URLs, OG URLs, sitemap, robots, CNAME, local links and local resources are present.");
