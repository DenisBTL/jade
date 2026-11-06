import { cpSync, mkdirSync, readFileSync, readdirSync, statSync, writeFileSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const root = path.dirname(fileURLToPath(import.meta.url));
const repository = process.env.GITHUB_REPOSITORY?.split("/").pop() || "jade";
if (!/^[a-zA-Z0-9._-]+$/.test(repository)) throw new Error("Nom de d?p?t invalide");
const base = repository.endsWith(".github.io") ? "" : `/${repository}`;
const destination = path.join(root, "outputs/pages");
mkdirSync(destination, { recursive: true });
cpSync(path.join(root, "dist"), destination, { recursive: true });
function rewrite(directory) {
  for (const entry of readdirSync(directory)) {
    const filename = path.join(directory, entry);
    if (statSync(filename).isDirectory()) rewrite(filename);
    else if (filename.endsWith(".html")) {
      const html = readFileSync(filename, "utf8").replace(/(\b(?:href|src)=['"])\/(?!\/)/g, `$1${base}/`);
      writeFileSync(filename, html);
    }
  }
}
rewrite(destination);
console.log(`Site pr?t dans outputs/pages avec le pr?fixe ${base || "/"}`);
