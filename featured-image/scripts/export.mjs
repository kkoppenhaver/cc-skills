// Render a featured-image card to a 2x PNG.
// Usage (run from the project's image dir, which has playwright installed):
//   node export.mjs <slug>        # renders <slug>.html -> <slug>.png
import { chromium } from 'playwright';
import { join } from 'path';

const slug = process.argv[2];
if (!slug) {
  console.error('Usage: node export.mjs <slug>   (renders <slug>.html -> <slug>.png)');
  process.exit(1);
}

const cwd = process.cwd();
const inputFile = join(cwd, `${slug}.html`);
const outputFile = join(cwd, `${slug}.png`);

const browser = await chromium.launch();
const context = await browser.newContext({
  viewport: { width: 1600, height: 1000 },
  deviceScaleFactor: 2, // 2x for crisp output
});
const page = await context.newPage();

await page.goto('file://' + inputFile);
await page.waitForLoadState('networkidle');
await page.waitForTimeout(600); // let web + local fonts paint

// The template's root card carries the fixed dimensions; screenshot just that.
const card = page.locator('#card');
await card.screenshot({ path: outputFile });

await browser.close();
console.log(`Wrote ${outputFile}`);
