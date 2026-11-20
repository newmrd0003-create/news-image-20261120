import * as fs from "node:fs";
import * as crypto from "node:crypto";
import * as path from "node:path";
import { fileURLToPath } from "node:url";

// Entry program: copy the front page built by gen_image.py to /output/entry.png.
// Byte-identical on every run: a plain file copy, no re-encoding, no clock.
// After the copy, verify the output is intact: same size and same sha256 as
// the source, so a truncated or corrupted copy fails loudly instead of
// silently shipping a broken front page.
const here = path.dirname(fileURLToPath(import.meta.url));
const src = path.join(here, "entry.png");
const outDir = "/output";
const dst = path.join(outDir, "entry.png");

const sha256 = (file: string): string =>
  crypto.createHash("sha256").update(fs.readFileSync(file)).digest("hex");

fs.mkdirSync(outDir, { recursive: true });
fs.copyFileSync(src, dst);

const srcStat = fs.statSync(src);
const dstStat = fs.statSync(dst);
if (dstStat.size !== srcStat.size) {
  throw new Error(
    `size mismatch after copy: src ${srcStat.size} bytes, dst ${dstStat.size} bytes`,
  );
}
const srcHash = sha256(src);
const dstHash = sha256(dst);
if (dstHash !== srcHash) {
  throw new Error(`sha256 mismatch after copy: src ${srcHash}, dst ${dstHash}`);
}
console.log(`wrote ${dst} (${dstStat.size} bytes, sha256 ${dstHash})`);
