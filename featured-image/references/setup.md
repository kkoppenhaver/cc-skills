# One-time project setup

Run this the first time a project needs featured images. It scaffolds the image dir, wires the brand, and installs the renderer. After it, generating images is just compose → render.

## 1. Choose the image dir

Default to `infographics/` at the repo root. If the repo already has a graphics dir (e.g. `assets/images/`, `infographics/`), use that instead.

## 2. Gather the brand

Infer first, ask second. Look for brand tokens in the repo before asking the user:
- site CSS / theme files, `tailwind.config.*`, CSS custom properties (`:root`)
- any existing infographic, social card, or design doc
- a `BRAND_GUIDE.md` / `docs/brand*`

Collect (and confirm with the user — propose inferred values rather than asking cold):
- **Colors:** background, surface/card, primary text, secondary text, accent, accent-dark (a darker accent for small text on light backgrounds), border.
- **Fonts:** heading font and an accent font (for the italic subhead). Note the source — a Google Fonts family, or local font files.
- **Footer/domain text** (optional), and **dimensions** (default 1280×720).

If local font files exist, copy them into `<image-dir>/fonts/`.

## 3. Scaffold the files

In the image dir, create:

- **`featured-image.json`** — marks the project configured and stores defaults:
  ```json
  {
    "brand": "BrandName",
    "dimensions": { "width": 1280, "height": 720 },
    "deviceScaleFactor": 2,
    "domain": "example.com",
    "fonts": { "heading": "Aileron", "accent": "Cardo" },
    "tokens": { "bg": "#fffff4", "text": "#283950", "accent": "#c2a990" }
  }
  ```
- **`brand-template.html`** — copy `assets/brand-template.html` from this skill, then fill in the `:root` tokens and wire the fonts (Google Fonts `<link>` or local `@font-face`). This is the canonical brand card; per-post images are copies of it.
- **`export.mjs`** — copy `scripts/export.mjs` from this skill (generic; no edits needed).
- **`package.json`**:
  ```json
  { "name": "<repo>-images", "private": true, "type": "module",
    "scripts": { "export": "node export.mjs" },
    "devDependencies": { "playwright": "^1.60.0" } }
  ```

## 4. Install the renderer

From the image dir: `npm install playwright`. The `node_modules/` is gitignored (add the rule if missing). Chromium is cached globally by Playwright, so if any project on the machine has run it before, no browser download happens.

If `npm install playwright` doesn't fetch a browser, run `npx playwright install chromium` once.

## 5. Test render

`node export.mjs brand-template`, then open/read `brand-template.png`. Confirm the brand fonts actually loaded (not fallback) and colors are right. Adjust `:root` tokens and font wiring until it looks on-brand. The project is now configured.
