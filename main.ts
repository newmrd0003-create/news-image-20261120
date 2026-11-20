import * as fs from "node:fs";
import * as path from "node:path";
import { fileURLToPath } from "node:url";

// Entry program: copy the front page built by gen_image.py to /output/entry.png.
// Byte-identical on every run: a plain file copy, no re-encoding, no clock.
const here = path.dirname(fileURLToPath(import.meta.url));
const src = path.join(here, "entry.png");
const outDir = "/output";
const dst = path.join(outDir, "entry.png");

fs.mkdirSync(outDir, { recursive: true });
fs.copyFileSync(src, dst);
console.log("wrote " + dst);
